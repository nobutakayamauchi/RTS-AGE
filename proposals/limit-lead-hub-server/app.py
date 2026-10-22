from __future__ import annotations

import csv
import hmac
import html
import io
import json
import os
import re
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

DB_PATH = Path(os.getenv("LLH_DB_PATH", "./data/limit-lead-hub.sqlite3"))
KIT_NAME = os.getenv("LLH_KIT_NAME", "限界開発スターターキット")
KIT_VERSION = os.getenv("LLH_KIT_VERSION", "v0.1.0")
KIT_URL = os.getenv("LLH_KIT_URL", "https://example.com/replace-me")
LINE_ADD_URL = os.getenv("LLH_LINE_ADD_URL", "")
X_PROFILE_URL = os.getenv("LLH_X_PROFILE_URL", "")
PRIVACY_POLICY_URL = os.getenv("LLH_PRIVACY_POLICY_URL", "")
ADMIN_USER = os.getenv("LLH_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("LLH_ADMIN_PASSWORD", "replace-me")
ADMIN_ACTION_TOKEN = os.getenv("LLH_ADMIN_ACTION_TOKEN", "replace-me")
CONSENT_TEXT_VERSION = "2026-08-01-v1"

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS leads (
  lead_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('ACTIVE','UNSUBSCRIBED','BLOCKED')),
  display_name TEXT NOT NULL DEFAULT '',
  email TEXT NOT NULL DEFAULT '',
  line_name TEXT NOT NULL DEFAULT '',
  x_handle TEXT NOT NULL DEFAULT '',
  preferred_channel TEXT NOT NULL CHECK(preferred_channel IN ('email','line','x')),
  channel_email INTEGER NOT NULL CHECK(channel_email IN (0,1)),
  channel_line INTEGER NOT NULL CHECK(channel_line IN (0,1)),
  channel_x INTEGER NOT NULL CHECK(channel_x IN (0,1)),
  consent_delivery INTEGER NOT NULL CHECK(consent_delivery IN (0,1)),
  consent_updates INTEGER NOT NULL CHECK(consent_updates IN (0,1)),
  consent_offers INTEGER NOT NULL CHECK(consent_offers IN (0,1)),
  consent_text_version TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT 'web',
  current_kit_version TEXT NOT NULL,
  unsubscribe_token TEXT NOT NULL UNIQUE,
  last_delivery_at TEXT,
  notes TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_leads_x_handle ON leads(x_handle);

CREATE TABLE IF NOT EXISTS deliveries (
  delivery_id TEXT PRIMARY KEY,
  lead_id TEXT NOT NULL REFERENCES leads(lead_id) ON DELETE CASCADE,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  channel TEXT NOT NULL CHECK(channel IN ('email','line','x')),
  destination TEXT NOT NULL DEFAULT '',
  kit_version TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('PENDING','MANUAL_REQUIRED','SENT','FAILED','CANCELLED')),
  attempts INTEGER NOT NULL DEFAULT 0,
  last_attempt_at TEXT,
  sent_at TEXT,
  error_code TEXT NOT NULL DEFAULT '',
  error_message TEXT NOT NULL DEFAULT '',
  operator_note TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_deliveries_status_channel
  ON deliveries(status, channel);
CREATE INDEX IF NOT EXISTS idx_deliveries_lead
  ON deliveries(lead_id);

CREATE TABLE IF NOT EXISTS audit (
  audit_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  actor TEXT NOT NULL,
  event_type TEXT NOT NULL,
  lead_id TEXT NOT NULL DEFAULT '',
  delivery_id TEXT NOT NULL DEFAULT '',
  details_json TEXT NOT NULL DEFAULT '{}'
);
"""


class LeadInput(BaseModel):
    display_name: str = Field(default="", max_length=100)
    email: str = Field(default="", max_length=254)
    line_name: str = Field(default="", max_length=100)
    x_handle: str = Field(default="", max_length=32)
    preferred_channel: str = "email"
    channel_email: bool = False
    channel_line: bool = False
    channel_x: bool = False
    consent_delivery: bool = False
    consent_updates: bool = False
    consent_offers: bool = False
    source: str = Field(default="web", max_length=80)
    notes: str = Field(default="", max_length=1000)
    website: str = Field(default="", max_length=200)


class AdminAction(BaseModel):
    note: str = Field(default="", max_length=500)


class UnsubscribeInput(BaseModel):
    token: str = Field(min_length=16, max_length=200)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_id(prefix: str) -> str:
    return f"{prefix}-{secrets.token_hex(6).upper()}"


def valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value))


def normalize_x_handle(value: str) -> str:
    value = value.strip().removeprefix("@")
    if value and not re.fullmatch(r"[A-Za-z0-9_]{1,15}", value):
        raise ValueError("Xアカウント名の形式が正しくありません。")
    return f"@{value}" if value else ""


@contextmanager
def db() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with db() as conn:
        conn.executescript(SCHEMA)


def audit(
    conn: sqlite3.Connection,
    actor: str,
    event_type: str,
    lead_id: str = "",
    delivery_id: str = "",
    details: dict[str, Any] | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO audit
        (audit_id, created_at, actor, event_type, lead_id, delivery_id, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            make_id("AUD"),
            now_iso(),
            actor,
            event_type,
            lead_id,
            delivery_id,
            json.dumps(details or {}, ensure_ascii=False, separators=(",", ":")),
        ),
    )


security = HTTPBasic(auto_error=False)


def require_admin(
    credentials: HTTPBasicCredentials | None = Depends(security),
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required.",
            headers={"WWW-Authenticate": 'Basic realm="Limit Lead Hub"'},
        )
    user_ok = hmac.compare_digest(credentials.username, ADMIN_USER)
    pass_ok = hmac.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials.",
            headers={"WWW-Authenticate": 'Basic realm="Limit Lead Hub"'},
        )
    return credentials.username


def require_action_token(request: Request) -> None:
    supplied = request.headers.get("x-admin-action-token", "")
    if not hmac.compare_digest(supplied, ADMIN_ACTION_TOKEN):
        raise HTTPException(status_code=403, detail="Admin action token is invalid.")


app = FastAPI(title="Limit Lead Hub", version="0.1.0")
init_db()


@app.get("/healthz")
def healthz() -> dict[str, Any]:
    with db() as conn:
        conn.execute("SELECT 1").fetchone()
    problems = []
    if ADMIN_PASSWORD == "replace-me":
        problems.append("LLH_ADMIN_PASSWORD")
    if ADMIN_ACTION_TOKEN == "replace-me":
        problems.append("LLH_ADMIN_ACTION_TOKEN")
    if "example.com/replace-me" in KIT_URL:
        problems.append("LLH_KIT_URL")
    return {
        "ok": True,
        "service": "limit-lead-hub",
        "kit_version": KIT_VERSION,
        "config_problems": problems,
    }


@app.get("/lead/apply", response_class=HTMLResponse)
def apply_page() -> str:
    privacy = (
        f'<a href="{html.escape(PRIVACY_POLICY_URL)}">取扱方針</a>'
        if PRIVACY_POLICY_URL
        else "取扱方針は公開前に設定されます"
    )
    return f"""<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(KIT_NAME)} 受取申請</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f6f7fb;color:#172033}}
main{{max-width:720px;margin:auto;padding:24px 16px 64px}}
.card{{background:#fff;border:1px solid #dfe3ea;border-radius:16px;padding:20px}}
label{{display:block;margin:14px 0 6px;font-weight:700}}
input,select,button{{font:inherit}} input[type=text],input[type=email],select{{width:100%;box-sizing:border-box;padding:12px;border:1px solid #bdc5d1;border-radius:10px}}
.choice{{display:flex;gap:10px;padding:12px 0;border-bottom:1px solid #edf0f4}} .small{{font-size:.9rem;color:#596579}}
button{{margin-top:18px;padding:13px 18px;border:0;border-radius:10px;background:#2458bb;color:#fff;font-weight:800}}
.result{{margin-top:18px;padding:14px;border-radius:10px;background:#eef6ff;white-space:pre-wrap}} .hp{{position:absolute;left:-9999px}}
</style></head><body><main>
<h1>AI開発・再開キット</h1>
<p>メール・LINE・Xから、受取窓口を最低一つ選んでください。複数選択できます。</p>
<section class="card"><form id="form">
<label>呼び名（任意）</label><input name="display_name" type="text">
<div class="choice"><input name="channel_email" type="checkbox"><div><b>メール</b><div class="small">更新版も確実に受け取りたい方向け</div></div></div>
<label>メールアドレス</label><input name="email" type="email">
<div class="choice"><input name="channel_line" type="checkbox"><div><b>LINE</b><div class="small">今回のキットを手軽に受け取りたい方向け</div></div></div>
<label>LINE表示名（任意）</label><input name="line_name" type="text">
<div class="choice"><input name="channel_x" type="checkbox"><div><b>X</b><div class="small">開発状況をライトに追いたい方向け</div></div></div>
<label>Xアカウント名</label><input name="x_handle" type="text" placeholder="@example">
<label>優先する受取方法</label><select name="preferred_channel"><option value="email">メール</option><option value="line">LINE</option><option value="x">X</option></select>
<div class="choice"><input name="consent_delivery" type="checkbox"><div><b>今回のキット送付に同意します（必須）</b></div></div>
<div class="choice"><input name="consent_updates" type="checkbox"><div>キット更新・互換性・差し替え情報を受け取る</div></div>
<div class="choice"><input name="consent_offers" type="checkbox"><div>新しい無料配布物やサービス案内を受け取る</div></div>
<input class="hp" name="website" type="text" tabindex="-1">
<p class="small">送信前に{privacy}をご確認ください。</p>
<button type="submit">受取申請を送る</button><div id="result" class="result" hidden></div>
</form></section></main>
<script>
const f=document.getElementById('form'),r=document.getElementById('result');
f.addEventListener('submit',async e=>{{e.preventDefault();const d=new FormData(f);const p={{display_name:d.get('display_name')||'',email:d.get('email')||'',line_name:d.get('line_name')||'',x_handle:d.get('x_handle')||'',preferred_channel:d.get('preferred_channel')||'email',channel_email:d.has('channel_email'),channel_line:d.has('channel_line'),channel_x:d.has('channel_x'),consent_delivery:d.has('consent_delivery'),consent_updates:d.has('consent_updates'),consent_offers:d.has('consent_offers'),source:'web',website:d.get('website')||''}};r.hidden=false;r.textContent='送信中…';try{{const x=await fetch('/api/leads',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify(p)}}),j=await x.json();if(!x.ok)throw new Error(j.detail||'申請できませんでした');r.textContent='受付番号: '+j.lead_id+'\n\n'+j.instructions.join('\n');f.reset();}}catch(err){{r.textContent=err.message;}}}});
</script></body></html>"""


@app.post("/api/leads")
def create_lead(data: LeadInput) -> JSONResponse:
    if data.website:
        raise HTTPException(status_code=400, detail="申請を受け付けられませんでした。")
    selected = [
        c for c, enabled in (
            ("email", data.channel_email),
            ("line", data.channel_line),
            ("x", data.channel_x),
        ) if enabled
    ]
    if not selected:
        raise HTTPException(status_code=400, detail="受取方法を最低一つ選んでください。")
    if not data.consent_delivery:
        raise HTTPException(status_code=400, detail="今回の送付に関する同意が必要です。")
    if data.channel_email and not valid_email(data.email.strip()):
        raise HTTPException(status_code=400, detail="メールアドレスを確認してください。")
    try:
        x_handle = normalize_x_handle(data.x_handle) if data.channel_x else ""
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if data.channel_x and not x_handle:
        raise HTTPException(status_code=400, detail="Xアカウント名を入力してください。")

    preferred = data.preferred_channel if data.preferred_channel in selected else selected[0]
    now = now_iso()
    lead_id = make_id("LD")
    token = secrets.token_urlsafe(32)
    instructions: list[str] = []

    with db() as conn:
        conn.execute(
            """INSERT INTO leads (
            lead_id,created_at,updated_at,status,display_name,email,line_name,x_handle,
            preferred_channel,channel_email,channel_line,channel_x,
            consent_delivery,consent_updates,consent_offers,consent_text_version,
            source,current_kit_version,unsubscribe_token,notes
            ) VALUES (?,?,?,'ACTIVE',?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                lead_id, now, now, data.display_name.strip(),
                data.email.strip().lower() if data.channel_email else "",
                data.line_name.strip() if data.channel_line else "", x_handle,
                preferred, int(data.channel_email), int(data.channel_line), int(data.channel_x),
                1, int(data.consent_updates), int(data.consent_offers), CONSENT_TEXT_VERSION,
                data.source.strip() or "web", KIT_VERSION, token, data.notes.strip(),
            ),
        )
        for channel in selected:
            destination = {"email": data.email.strip().lower(), "line": data.line_name.strip(), "x": x_handle}[channel]
            delivery_id = make_id("DLV")
            delivery_status = "PENDING" if channel == "email" else "MANUAL_REQUIRED"
            conn.execute(
                """INSERT INTO deliveries
                (delivery_id,lead_id,created_at,updated_at,channel,destination,kit_version,status)
                VALUES (?,?,?,?,?,?,?,?)""",
                (delivery_id, lead_id, now, now, channel, destination, KIT_VERSION, delivery_status),
            )
            if channel == "email":
                instructions.append("メール送信キューへ登録しました。送信アダプター接続までは安全に保留されます。")
            elif channel == "line":
                instructions.append(f'LINEから「KIT {lead_id}」と送ってください。')
            else:
                instructions.append(f'XのDMまたは返信で「KIT {lead_id}」と送ってください。')
        audit(conn, "PUBLIC_FORM", "LEAD_CREATED", lead_id=lead_id, details={"channels": selected, "preferred": preferred})

    return JSONResponse({"ok": True, "lead_id": lead_id, "kit_version": KIT_VERSION, "instructions": instructions, "line_add_url": LINE_ADD_URL, "x_profile_url": X_PROFILE_URL}, status_code=201)


@app.get("/lead/admin", response_class=HTMLResponse)
def admin_page(_: str = Depends(require_admin)) -> str:
    with db() as conn:
        rows = conn.execute(
            """SELECT d.*,l.display_name,l.email,l.line_name,l.x_handle,l.status AS lead_status
            FROM deliveries d JOIN leads l ON l.lead_id=d.lead_id
            ORDER BY CASE d.status WHEN 'MANUAL_REQUIRED' THEN 0 WHEN 'PENDING' THEN 1 WHEN 'FAILED' THEN 2 ELSE 3 END,
            d.created_at DESC LIMIT 300"""
        ).fetchall()
        lead_count = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        pending_count = conn.execute("SELECT COUNT(*) FROM deliveries WHERE status IN ('PENDING','MANUAL_REQUIRED','FAILED')").fetchone()[0]
    body = []
    for row in rows:
        body.append(
            f"<tr><td>{html.escape(row['created_at'])}</td><td><code>{html.escape(row['lead_id'])}</code></td>"
            f"<td>{html.escape(row['channel'])}</td><td>{html.escape(row['destination'] or '(未入力)')}</td>"
            f"<td><b>{html.escape(row['status'])}</b></td><td>{html.escape(row['kit_version'])}</td>"
            f"<td><button onclick=\"markIt('{html.escape(row['delivery_id'])}','sent')\">送付済み</button> "
            f"<button onclick=\"markIt('{html.escape(row['delivery_id'])}','failed')\">失敗</button></td></tr>"
        )
    token = json.dumps(ADMIN_ACTION_TOKEN)
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Limit Lead Hub 管理</title><style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f5f7fb;color:#172033}}main{{max-width:1200px;margin:auto;padding:20px 14px 60px}}table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{padding:10px;border-bottom:1px solid #e6eaf0;text-align:left}}button,a{{padding:8px 10px;border:0;border-radius:8px;background:#2356b6;color:#fff;text-decoration:none}}.scroll{{overflow-x:auto}}
</style></head><body><main><h1>Limit Lead Hub 管理</h1><p>リード {lead_count}件／要対応 {pending_count}件</p><p><a href="/lead/export.csv">CSV出力</a></p><div class="scroll"><table><thead><tr><th>受付日時</th><th>受付番号</th><th>方法</th><th>宛先</th><th>状態</th><th>版</th><th>操作</th></tr></thead><tbody>{''.join(body)}</tbody></table></div><p id="message"></p></main><script>
const t={token};async function markIt(id,a){{const note=prompt('記録メモ（任意）','')||'';const x=await fetch(`/api/admin/deliveries/${{id}}/${{a}}`,{{method:'POST',headers:{{'content-type':'application/json','x-admin-action-token':t}},body:JSON.stringify({{note}})}}),j=await x.json();document.getElementById('message').textContent=x.ok?'更新しました':(j.detail||'失敗');if(x.ok)location.reload();}}
</script></body></html>"""


@app.post("/api/admin/deliveries/{delivery_id}/{action}")
def update_delivery(delivery_id: str, action: str, data: AdminAction, request: Request, admin: str = Depends(require_admin)) -> dict[str, Any]:
    require_action_token(request)
    if action not in {"sent", "failed"}:
        raise HTTPException(status_code=400, detail="Unknown action.")
    with db() as conn:
        row = conn.execute("SELECT * FROM deliveries WHERE delivery_id=?", (delivery_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Delivery not found.")
        now = now_iso()
        new_status = "SENT" if action == "sent" else "FAILED"
        sent_at = now if action == "sent" else None
        conn.execute(
            """UPDATE deliveries SET status=?,updated_at=?,attempts=attempts+1,last_attempt_at=?,sent_at=?,operator_note=?,error_code=?,error_message=? WHERE delivery_id=?""",
            (new_status, now, now, sent_at, data.note.strip(), "" if action == "sent" else "MANUAL_FAILURE", "" if action == "sent" else data.note.strip(), delivery_id),
        )
        if action == "sent":
            conn.execute("UPDATE leads SET updated_at=?,last_delivery_at=? WHERE lead_id=?", (now, now, row["lead_id"]))
        audit(conn, admin, f"DELIVERY_MARKED_{new_status}", row["lead_id"], delivery_id, {"channel": row["channel"], "note": data.note.strip()})
    return {"ok": True, "delivery_id": delivery_id, "status": new_status}


@app.get("/lead/export.csv")
def export_csv(_: str = Depends(require_admin)) -> StreamingResponse:
    output = io.StringIO()
    headers = ["lead_id","created_at","status","display_name","email","line_name","x_handle","preferred_channel","consent_delivery","consent_updates","consent_offers","current_kit_version","last_delivery_at"]
    writer = csv.writer(output); writer.writerow(headers)
    with db() as conn:
        for row in conn.execute(f"SELECT {','.join(headers)} FROM leads ORDER BY created_at DESC"):
            writer.writerow([row[h] for h in headers])
    return StreamingResponse(iter([output.getvalue().encode("utf-8-sig")]), media_type="text/csv; charset=utf-8", headers={"Content-Disposition": 'attachment; filename="limit-leads.csv"'})


@app.get("/lead/unsubscribe", response_class=HTMLResponse)
def unsubscribe_page(token: str = "") -> str:
    with db() as conn:
        exists = bool(token and conn.execute("SELECT 1 FROM leads WHERE unsubscribe_token=?", (token,)).fetchone())
    button = '<button id="confirm">配信を停止する</button>' if exists else ''
    msg = "下のボタンを押すと更新情報と案内を停止します。" if exists else "停止対象が見つかりません。"
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>配信停止</title></head><body><main><h1>配信停止</h1><p>{html.escape(msg)}</p>{button}<p id="r"></p></main><script>const t={json.dumps(token)},b=document.getElementById('confirm');if(b)b.onclick=async()=>{{const x=await fetch('/api/unsubscribe',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify({{token:t}})}}),j=await x.json();document.getElementById('r').textContent=x.ok?j.message:(j.detail||'処理できませんでした');}};</script></body></html>"""


@app.post("/api/unsubscribe")
def unsubscribe(data: UnsubscribeInput) -> dict[str, Any]:
    with db() as conn:
        lead = conn.execute("SELECT * FROM leads WHERE unsubscribe_token=?", (data.token,)).fetchone()
        if lead is None:
            raise HTTPException(status_code=404, detail="停止対象が見つかりません。")
        now = now_iso()
        conn.execute("UPDATE leads SET status='UNSUBSCRIBED',updated_at=?,consent_updates=0,consent_offers=0 WHERE lead_id=?", (now, lead["lead_id"]))
        conn.execute("UPDATE deliveries SET status='CANCELLED',updated_at=?,error_code='UNSUBSCRIBED',error_message='Cancelled after unsubscribe.' WHERE lead_id=? AND channel='email' AND status='PENDING'", (now, lead["lead_id"]))
        audit(conn, "PUBLIC_UNSUBSCRIBE", "ALL_UNSUBSCRIBED", lead["lead_id"])
    return {"ok": True, "message": "更新情報と案内の配信停止を受け付けました。"}

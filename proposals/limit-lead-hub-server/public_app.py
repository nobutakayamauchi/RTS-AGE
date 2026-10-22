from __future__ import annotations

import html
import json

from fastapi import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app import (
    KIT_NAME,
    KIT_URL,
    LINE_ADD_URL,
    PRIVACY_POLICY_URL,
    X_PROFILE_URL,
    LeadInput,
    create_lead as create_lead_base,
)
from kit_app import app


# Replace the prototype intake routes while retaining the ledger, admin,
# unsubscribe, kit, privacy, and health routes from app.py / kit_app.py.
for route in list(app.router.routes):
    if getattr(route, "path", "") in {"/lead/apply", "/api/leads"}:
        app.router.routes.remove(route)


@app.get("/lead/apply", response_class=HTMLResponse)
def public_apply_page() -> str:
    privacy = (
        f'<a href="{html.escape(PRIVACY_POLICY_URL)}">取扱方針</a>'
        if PRIVACY_POLICY_URL
        else "取扱方針"
    )
    line_note = (
        '<p class="small">LINE連携は現在利用できます。</p>'
        if LINE_ADD_URL
        else '<p class="small">LINE受取は準備中です。</p>'
    )
    x_note = (
        '<p class="small">X連携は現在利用できます。</p>'
        if X_PROFILE_URL
        else '<p class="small">X受取は準備中です。</p>'
    )
    kit_url_json = json.dumps(KIT_URL)
    return f"""<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(KIT_NAME)} 受取申請</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f6f7fb;color:#172033}}
main{{max-width:720px;margin:auto;padding:24px 16px 64px}}
.card{{background:#fff;border:1px solid #dfe3ea;border-radius:16px;padding:20px}}
label{{display:block;margin:14px 0 6px;font-weight:700}}
input,button{{font:inherit}} input[type=text],input[type=email]{{width:100%;box-sizing:border-box;padding:12px;border:1px solid #bdc5d1;border-radius:10px}}
.choice{{display:flex;gap:10px;padding:12px 0;border-bottom:1px solid #edf0f4}} .small{{font-size:.9rem;color:#596579}}
button{{margin-top:18px;padding:13px 18px;border:0;border-radius:10px;background:#2458bb;color:#fff;font-weight:800}}
.result{{margin-top:18px;padding:14px;border-radius:10px;background:#eef6ff;white-space:pre-wrap}}
.result a{{display:inline-block;margin-top:12px;padding:12px 16px;border-radius:9px;background:#2458bb;color:#fff;text-decoration:none;font-weight:800}}
.hp{{position:absolute;left:-9999px}}
</style></head><body><main>
<h1>AI開発・再開キット</h1>
<p>メールアドレスを登録すると、この画面からスターターキットをすぐ受け取れます。</p>
<section class="card"><form id="form">
<label>呼び名（任意）</label><input name="display_name" type="text">
<label>メールアドレス</label><input name="email" type="email" required autocomplete="email">
<div class="choice"><input name="consent_delivery" type="checkbox" required><div><b>今回のキット受取と、そのための連絡先登録に同意します（必須）</b></div></div>
<div class="choice"><input name="consent_updates" type="checkbox"><div>キット更新・互換性・差し替え情報を受け取る</div></div>
<div class="choice"><input name="consent_offers" type="checkbox"><div>新しい無料配布物やサービス案内を受け取る</div></div>
<input class="hp" name="website" type="text" tabindex="-1" autocomplete="off">
<p class="small">送信前に{privacy}をご確認ください。</p>
{line_note}{x_note}
<button type="submit">登録してキットを受け取る</button><div id="result" class="result" hidden></div>
</form></section></main>
<script>
const f=document.getElementById('form'),r=document.getElementById('result'),fallbackKit={kit_url_json};
f.addEventListener('submit',async e=>{{
  e.preventDefault();
  const d=new FormData(f);
  const p={{
    display_name:d.get('display_name')||'',email:d.get('email')||'',line_name:'',x_handle:'',
    preferred_channel:'email',channel_email:true,channel_line:false,channel_x:false,
    consent_delivery:d.has('consent_delivery'),consent_updates:d.has('consent_updates'),
    consent_offers:d.has('consent_offers'),source:'web',website:d.get('website')||''
  }};
  r.hidden=false;r.textContent='送信中…';
  try{{
    const x=await fetch('/api/leads',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify(p)}});
    const j=await x.json();if(!x.ok)throw new Error(j.detail||'申請できませんでした');
    r.textContent='受付番号: '+j.lead_id+'\n\n受付が完了しました。';
    const a=document.createElement('a');a.href=j.kit_url||fallbackKit;a.textContent='スターターキットをダウンロード';
    r.appendChild(document.createElement('br'));r.appendChild(a);f.reset();
  }}catch(err){{r.textContent=err.message;}}
}});
</script></body></html>"""


@app.post("/api/leads")
def public_create_lead(data: LeadInput) -> JSONResponse:
    if data.channel_line and not LINE_ADD_URL:
        raise HTTPException(status_code=400, detail="LINE受取は現在準備中です。")
    if data.channel_x and not X_PROFILE_URL:
        raise HTTPException(status_code=400, detail="X受取は現在準備中です。")

    response = create_lead_base(data)
    payload = json.loads(response.body.decode("utf-8"))
    payload["kit_url"] = KIT_URL
    payload["instructions"] = [
        "受付が完了しました。キットはこの画面からすぐ受け取れます。"
    ] + [
        item for item in payload.get("instructions", [])
        if not item.startswith("メール送信キュー")
    ]
    return JSONResponse(payload, status_code=response.status_code)

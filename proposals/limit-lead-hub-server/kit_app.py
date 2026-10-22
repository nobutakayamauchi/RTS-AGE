from __future__ import annotations

import html
import io
import zipfile
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import HTMLResponse, Response

from app import KIT_NAME, KIT_VERSION, app

APP_ROOT = Path(__file__).resolve().parent
KIT_DIR = APP_ROOT / "kit"


@app.get("/kit", response_class=HTMLResponse)
def kit_page() -> str:
    return f"""<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(KIT_NAME)}</title>
<style>body{{font-family:system-ui,sans-serif;margin:0;background:#f6f7fb;color:#172033}}main{{max-width:720px;margin:auto;padding:28px 16px 64px}}section{{background:#fff;border:1px solid #dfe3ea;border-radius:16px;padding:22px}}a.button{{display:inline-block;padding:13px 18px;border-radius:10px;background:#2458bb;color:#fff;text-decoration:none;font-weight:800}}li{{margin:.7em 0}}</style>
</head><body><main><section>
<h1>{html.escape(KIT_NAME)}</h1>
<p>版: {html.escape(KIT_VERSION)}</p>
<p>長いAI開発を中断後でも再開できるように、現在地・次の一手・判断・復旧情報を残すためのテンプレート集です。</p>
<ul><li>プロジェクト現在地シート</li><li>次の一手シート</li><li>判断ログ</li><li>AI引継ぎプロンプト</li><li>RTS-Liteテンプレート</li><li>停止・再開チェックリスト</li></ul>
<p><a class="button" href="/kit/latest">最新版ZIPを受け取る</a></p>
</section></main></body></html>"""


@app.get("/kit/latest")
def download_latest_kit() -> Response:
    files = sorted(path for path in KIT_DIR.rglob("*") if path.is_file())
    if not files:
        raise HTTPException(status_code=503, detail="配布キットがまだ準備されていません。")

    root_name = f"limit-development-starter-kit-{KIT_VERSION.lstrip('v')}"
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            relative = path.relative_to(KIT_DIR)
            archive.write(path, f"{root_name}/{relative.as_posix()}")
        archive.writestr(
            f"{root_name}/VERSION.txt",
            f"{KIT_NAME}\nversion={KIT_VERSION}\n",
        )

    filename = f"limit-development-starter-kit-{KIT_VERSION}.zip"
    return Response(
        content=buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )


@app.get("/lead/privacy", response_class=HTMLResponse)
def privacy_page() -> str:
    return f"""<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>受取申請情報の取扱方針</title>
<style>body{{font-family:system-ui,sans-serif;margin:0;background:#f6f7fb;color:#172033}}main{{max-width:760px;margin:auto;padding:28px 16px 64px}}section{{background:#fff;border:1px solid #dfe3ea;border-radius:16px;padding:22px}}h2{{margin-top:1.6em}}</style>
</head><body><main><section>
<h1>受取申請情報の取扱方針</h1>
<p>対象: {html.escape(KIT_NAME)} / 方針版: 2026-08-01-v1</p>
<h2>取得する情報</h2>
<p>申請者が選んだメールアドレス、LINE表示名、Xアカウント名、呼び名、受取方法、各種同意、受付・送付履歴を取得します。最低一つの連絡先が必要です。</p>
<h2>利用目的</h2>
<p>今回のキット送付、申請者が同意した更新情報または案内の提供、送付状況の管理、不正利用防止、障害対応のために利用します。</p>
<h2>同意の分離</h2>
<p>今回の送付、更新情報、サービス案内は別々に管理します。更新情報または案内の停止後も、法令対応や監査に必要な最小記録を保持する場合があります。</p>
<h2>第三者提供と販売</h2>
<p>取得情報を広告目的で販売しません。法令上必要な場合を除き、本人の同意なく第三者へ提供しません。将来、メール配信事業者などを利用する場合は、利用目的の範囲内で必要最小限の情報を委託します。</p>
<h2>安全管理</h2>
<p>連絡先と送付履歴はサーバー内の台帳で管理し、管理画面には認証を設けます。秘密情報や実データを公開リポジトリへ保存しません。</p>
<h2>停止・訂正・削除</h2>
<p>配信停止用ページから更新情報と案内を停止できます。訂正や削除の連絡窓口は、公開前に申請ページまたは案内文へ明示します。</p>
<h2>改定</h2>
<p>内容を変更した場合は方針版を更新し、重要な変更は適切な方法で知らせます。</p>
</section></main></body></html>"""

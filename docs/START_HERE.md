# RTS-AGE Documentation Start Here

このページは、現在のRTS-AGE環境を理解し、安全に作業を再開するための入口です。

## 最初に読む順番

1. [`startup/BEGINNER_STARTUP_GUIDE.md`](startup/BEGINNER_STARTUP_GUIDE.md)
   - 初心者向けに、何がどこで動き、普段の作業が何を意味するのかを説明します。
2. [`operations/CURRENT_ENVIRONMENT.md`](operations/CURRENT_ENVIRONMENT.md)
   - 現在確認できているサーバー、サービス、接続、安全境界、候補環境の状態を記録します。
3. [`operations/ENVIRONMENT_CHANGELOG.md`](operations/ENVIRONMENT_CHANGELOG.md)
   - OS更新、接続変更、認証追加、候補版検証などの環境変更を日付順に残します。
4. [`STATUS.md`](STATUS.md)
   - RTS-AGEリポジトリ自体の役割と現在の位置づけを確認します。
5. [`NEXT.md`](NEXT.md)
   - 次に行う最小で安全な作業を確認します。

## この文書群の役割

この文書群は、コードの説明書だけではありません。

- いま何が本番で動いているか
- 何が候補環境で試験中か
- 何を変更したか
- どこまで確認済みか
- 何がまだ未確認か
- 初心者が次に何を見ればよいか

を分離して残すための運用記録です。

## 更新ルール

- APIキー、認証トークン、秘密鍵、個人情報は書かない。
- 確認済み、推定、未確認を混ぜない。
- 本番変更の前後で `CURRENT_ENVIRONMENT.md` を更新する。
- 環境変更を行ったら `ENVIRONMENT_CHANGELOG.md` に追記する。
- 作業途中の場合は、成功したことだけを確定事項として書き、実行中の作業は `PENDING` と明記する。
- コード変更と運用文書変更は、可能な限り小さなPRに分ける。

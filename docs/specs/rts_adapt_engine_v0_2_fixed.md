# RTS Adapt Engine 仕様書 v0.2 Fixed

人間性能に頼らない適応型AIワークフローエンジン

---

## 1. 概要

RTS Adapt Engine は、人間の記憶力・継続力・確認能力・文章作成能力・設計能力に過度に依存せず、AIによって作業の下準備・構成・成果物生成・導線設計・確認ポイント抽出を行うための適応型AIワークフローエンジンである。

本システムは、AIに責任を移すものではない。
AIが作業を準備・生成・整理し、人間が最終確認・承認・公開判断・責任を持つ。

---

## 2. 基本思想

人間は疲れる。忘れる。抜け漏れる。継続できない。
したがって、人間性能に頼り切ったプロジェクト設計をやめる。

RTS Adapt Engine は以下の思想で設計する。

- 人間性能への依存度を下げる
- 人間の認知負荷を下げる
- 苦手な作業はAIに委任する
- 人間は判断・承認・責任に集中する
- 作業工程をログ化する
- 出力物を再構成可能にする
- すべての成果物に確認ポイントを付ける
- 自動化より先に、承認可能な下書き生成を優先する
- 完全自動ではなく、半自動ワークフローを基本とする

---

## 3. 一文での定義

RTS Adapt Engine は、ユーザーのメモ・状況・目的・制約を読み取り、発信・営業・LINE公式導線・動画台本・商品設計・開発ログなどの成果物に変換し、人間が確認すべきポイントを抽出するAIワークフローエンジンである。

---

## 4. 対象領域

RTS Adapt Engine は、最終的に以下を扱う。

### 4.1 発信支援

- X投稿案
- Threads投稿案
- Bluesky投稿案
- Mastodon投稿案
- note下書き
- LINE配信文
- YouTube / Shorts / TikTok用台本
- 音声配信用台本
- 投稿タイトル案
- フック案
- 返信方針
- 炎上・誤解リスク抽出

### 4.2 LINE公式外箱設計

- 登録直後メッセージ
- あいさつメッセージ
- リッチメニュー設計
- ボタン別応答設計
- クイックリプライ設計
- 自動応答メッセージ設計
- 無料配布導線
- 相談導線
- 商品導線
- note / X / GitHub への誘導
- 配信シナリオ
- ステップ配信案
- FAQ応答案

### 4.3 商品・サービス導線設計

- 無料オファー
- フロント商品
- 本命商品
- 相談導線
- 申し込み導線
- アンケート導線
- 決済前説明文
- 納品物テンプレート
- 顧客への案内文

### 4.4 営業支援

- 営業先リスト用メモ整理
- 営業メール文
- DM文
- 問い合わせフォーム文
- フォローアップ文
- 業種別提案文
- 断られた後の返信案
- 相手別の訴求整理

### 4.5 開発ログ・RTS連携

- 今日の作業ログ
- 詰まりポイント
- 判断ログ
- 実装メモ
- 仕様変更ログ
- 実験ログ
- 失敗ログ
- 次の一手
- RTS再構成用ログ

### 4.6 動画・音声素材設計

- 2分動画台本
- 固定背景動画用原稿
- 字幕用短文
- 読み上げ用原稿
- 冒頭フック
- サムネ文言
- タイトル案
- 概要欄
- 次回予告

---

## 5. 基本構成

```text
RTS Adapt Engine
├─ Input Layer
├─ Context Normalizer
├─ Weakness / Constraint Mapper
├─ Workflow Planner
├─ Canonical Content Model
├─ Output Generator
├─ LINE Flow Builder
├─ SNS / Platform Extensibility Layer
├─ Review Extractor
├─ Approval Gate
├─ Connector Layer
├─ API Usage Safety Layer
├─ Execution Logger
└─ RTS Integration Layer
```

---

## 6. Input Layer

ユーザーの入力を受け取る層。

### 入力形式

v0.1では Markdown のみ対応する。
将来的には以下に対応する。

- Markdown
- テキストメモ
- 音声文字起こし
- URL
- GitHubログ
- X投稿ログ
- note下書き
- 画像メモ
- 既存LINE公式設定メモ
- 商品情報
- 営業先情報

### v0.1入力ファイル

```text
inputs/daily_input.md
```

### daily_input.md の基本項目

```markdown
# 今日の現状
# 今日やったこと
# 詰まっていること
# 次にやること
# 使いたいネタ
# 参考URL
# 言いたいこと
# 言ってはいけないこと
# 出力したい媒体
# 今日の温度感
# 売りたい商品・サービス
# 誘導したい行動
# LINE公式でやりたいこと
# 無料配布物
# 相談導線
# 注意事項
```

---

## 7. Context Normalizer

ぐちゃぐちゃな入力を整理する層。

### 役割

入力内容を以下に分解する。

- 現状
- 問題
- 制約
- 感情
- ネタ
- 商品
- 誘導先
- 禁止事項
- 使える素材
- 足りない情報
- 次の一手

### 出力

```text
outputs/context_summary.md
```

---

## 8. Weakness / Constraint Mapper

ユーザーの弱点・制約・認知負荷を整理する層。

### 役割

以下を判定する。

- 継続負荷が高い作業
- 確認ミスが出やすい作業
- 毎回ゼロから考えている作業
- AIに任せられる作業
- 人間が見るべき作業
- 自動化すべき作業
- 今は捨てるべき作業

### 出力

```text
outputs/constraint_map.md
```

---

## 9. Workflow Planner

入力内容から、その日に作るべき成果物を決める層。

### 役割

以下を決める。

- 今日出すべきX投稿
- Threads / Bluesky / Mastodon に展開できる投稿
- noteにすべき内容
- LINEで配るべき内容
- 動画化すべき内容
- 商品導線に回すべき内容
- 今は出さない方がいい内容
- 次に作るべき仕組み

### 出力

```text
outputs/workflow_plan.md
```

---

## 10. Canonical Content Model

特定SNSや媒体に依存しない、共通の成果物形式を定義する。

RTS Adapt Engine は、最初からX用・LINE用・note用に直接出力するのではなく、まず共通形式のコンテンツを作り、その後Platform Adapterで各媒体向けに変換する。

### 例

```yaml
id: generated_content_id
content_type: short_post
body: 投稿本文
hook: 冒頭の引き
cta: 誘導文
target_audience: 想定読者
hashtags: []
links: []
media:
  images: []
  video: null
  audio: null
risk_level: low
approval_status: draft
platform_candidates:
  - x
  - threads
  - bluesky
  - line
created_at: auto
```

---

## 11. Output Generator

媒体別に成果物を作る層。

### 出力候補

```text
outputs/
├─ x_posts.md
├─ threads_posts.md
├─ bluesky_posts.md
├─ mastodon_posts.md
├─ note_draft.md
├─ line_message.md
├─ video_script.md
├─ sales_copy.md
├─ product_offer.md
├─ dev_log.md
└─ summary.md
```

---

## 12. SNS / Platform Extensibility Layer

RTS Adapt Engine は、特定のSNSや配信媒体に依存しない設計とする。

X、Threads、Bluesky、Mastodon、note、LINE、YouTubeなど、既存媒体および将来登場する新規SNSへ後から接続できることを前提に設計する。

### 基本方針

- コアエンジンは特定SNSの仕様に依存しない
- まず共通形式の成果物を生成する
- 各SNSへの変換は Platform Adapter が担当する
- 外部投稿や配信は Connector が担当する
- API連携は承認済み出力のみを対象とする
- API仕様は実装時点で公式ドキュメントを確認する
- 未対応SNSでも、手動投稿用Markdown出力は可能にする

### Platform Adapter

各Adapterは以下を定義する。

- platform_id
- platform_name
- max_text_length
- supported_media
- supports_hashtags
- supports_links
- supports_scheduling
- supports_api_publish
- requires_manual_review
- output_format
- connector_status

### Capability Matrix

```yaml
platforms:
  x:
    enabled: false
    output_only: true
    api_publish: future
    adapter: x_adapter
  threads:
    enabled: false
    output_only: true
    api_publish: future
    adapter: threads_adapter
  bluesky:
    enabled: false
    output_only: true
    api_publish: future
    adapter: bluesky_adapter
  mastodon:
    enabled: false
    output_only: true
    api_publish: future
    adapter: mastodon_adapter
  line:
    enabled: true
    output_only: true
    api_publish: future
    adapter: line_adapter
  note:
    enabled: true
    output_only: true
    api_publish: future
    adapter: note_adapter
```

### Future Platform Policy

新規SNSが登場した場合は、Core Engineを変更せず、以下を追加する。

1. Platform Adapter
2. Capability Matrix の項目
3. Output Template
4. Connector
5. Review Rule

これにより、未知の媒体が追加されてもRTS Adapt Engine本体を壊さず拡張できるようにする。

---

## 13. LINE Flow Builder

LINE公式の外箱を設計するモジュール。

### 目的

LINE公式を、単なる配信先ではなく、無料配布・相談・商品販売・開発ログ共有の導線として設計する。

### 出力ファイル

```text
outputs/line_flow/
├─ line_flow_spec.md
├─ rich_menu_spec.md
├─ auto_reply_spec.md
├─ quick_reply_spec.md
├─ welcome_message.md
├─ delivery_sequence.md
├─ freebie_delivery.md
├─ consultation_flow.md
├─ product_flow.md
└─ faq_reply_spec.md
```

### リッチメニュー設計例

```text
リッチメニュー
├─ 無料テンプレ
├─ はじめに
├─ 相談する
├─ 商品一覧
├─ 開発ログ
└─ 最新note
```

### 各ボタンに定義する項目

- ボタン名
- 表示文言
- 押した時の挙動
- 返信メッセージ
- 誘導先URL
- 次に押してほしいボタン
- 関連する商品
- 注意事項

### v0.1での扱い

v0.1ではAPI連携はしない。
LINE公式管理画面に手動で設定できる仕様書を生成するだけにする。

---

## 14. Review Extractor

人間が確認すべきポイントを抽出する層。

### 出力ファイル

```text
outputs/review_checklist.md
```

### 確認項目

- 事実確認が必要な箇所
- 誇張表現
- 誤解されそうな表現
- 個人情報
- 機密情報
- 法的・倫理的に注意すべき表現
- 炎上リスク
- クライアント情報
- 断定しすぎている表現
- 出してはいけない可能性がある情報
- LINEで送るには強すぎる表現
- 商品案内として弱すぎる表現
- 誘導が不自然な箇所

---

## 15. Approval Gate

人間が承認する層。

AIが作ったものを、そのまま外部公開しない。

### 承認ステータス

```text
draft
needs_review
approved
exported
published
rejected
archived
```

### 承認ログ

```text
logs/approval_log.jsonl
```

### 記録項目

- 出力ファイル
- 承認状態
- 修正有無
- 却下理由
- 公開先
- 公開日時
- 人間のコメント

---

## 16. Connector Layer

外部サービスと接続する層。

### v0.1では実装しない

最初はMarkdown出力のみ。

### 将来のコネクタ

- Markdown Connector
- GitHub Connector
- Google Drive Connector
- Gmail Connector
- X Connector
- Threads Connector
- Bluesky Connector
- Mastodon Connector
- note Connector
- LINE Official Connector
- YouTube Connector
- Google Sheets Connector
- Notion Connector
- Calendar Connector
- Future Platform Connector

### 原則

- 最初は下書き保存まで
- 自動投稿は後回し
- 承認済みのみ外部送信可能
- API仕様は実装時に公式ドキュメントを確認する
- 認証情報はコード内に直書きしない

---

## 17. API Usage Safety / Rate Limit Policy

RTS Adapt Engine は、外部サービスのAPIを過剰に呼び出さない設計とする。

外部APIは、投稿・配信・取得・同期のために必要な場合のみ使用し、可能な限り以下の順序を優先する。

1. ローカル生成
2. Markdown / JSON 出力
3. 手動設定
4. 下書き作成
5. 承認済みデータのみAPI送信
6. 自動投稿・自動配信

### 基本方針

- APIを過剰に叩かない
- ポーリングよりWebhookを優先する
- 同じ情報を何度も取得しない
- キャッシュを使う
- 差分取得を優先する
- 失敗時に無限リトライしない
- 429 / rate limit / quota error を検知したら停止する
- 各プラットフォームの利用規約と公式API仕様を確認する
- APIキー・トークンをコードやログに残さない
- 承認前の投稿・配信をAPI送信しない

### API Call Budget

```yaml
api_budget:
  per_minute: 5
  per_hour: 30
  per_day: 100
  burst_limit: 3
  cooldown_seconds: 60
```

実際の上限値は、各プラットフォームの公式仕様に合わせて設定する。

### Backoff Policy

APIエラー発生時は、即時連続リトライを禁止する。

```text
1回目失敗 → 30秒待機
2回目失敗 → 2分待機
3回目失敗 → 10分待機
4回目失敗 → connector停止
```

429、rate limit、quota exceeded が返った場合は、即座にConnectorを一時停止する。

### Connector Execution Modes

```text
disabled      API連携しない
dry_run       API送信せず、送信予定内容だけ表示
manual_export Markdown / JSON / CSVで出力
draft_only    下書き作成のみ
approved_send 承認済みのみ送信
auto_send     将来対応。原則デフォルト禁止
```

デフォルトは dry_run または manual_export とする。
auto_send はv0.1〜v0.3では使用しない。

### Publishing Policy

```yaml
publishing_policy:
  default_mode: manual_export
  api_default: disabled
  max_public_posts_per_day:
    x: 2
    threads: 2
    bluesky: 2
    mastodon: 2
    note: 1
    line_broadcast: 1
  min_interval_minutes:
    short_sns: 180
    line_broadcast: 720
  require_human_approval: true
  duplicate_content_block: true
  auto_like: false
  auto_follow: false
  auto_dm: false
  auto_reply_to_random_users: false
```

---

## 18. Execution Logger

すべての実行をログ化する層。

### 出力ファイル

```text
logs/execution_log.jsonl
```

### 記録項目

- 実行日時
- 入力ファイル
- 使用モード
- 生成ファイル
- エラー有無
- 確認項目数
- 出力要約
- 次の推奨アクション

### APIログ

APIを呼び出した場合は、以下に記録する。

```text
logs/api_call_log.jsonl
```

ただし、APIキー・アクセストークン・認証情報・個人情報はログに残さない。

---

## 19. RTS Integration Layer

RTS本体と接続する層。

### 目的

RTS Adapt Engine の実行結果を、RTSの再構成可能ログとして扱う。

### 出力候補

```text
rts/
├─ sessions/
├─ manifests/
├─ evidence_snapshots/
├─ reconstruction.md
└─ decision_log.jsonl
```

### 役割

- 作業ログ保存
- 判断ログ保存
- 出力物のハッシュ化
- 変更履歴の保存
- 再構成用メモ生成
- RTS-AGEへのフィードバック

---

## 20. モード設計

AIへの委任率を切り替えられるようにする。

### Low Assist Mode

AIは整理と提案のみ行う。
人間が主に作る。

### Standard Mode

AIが叩き台を作り、人間が調整する。

### High Assist Mode

AIがほぼ完成形を作り、人間は確認と承認に集中する。

### Emergency Mode

疲労・時間不足・メンタル低下時のモード。
出力を減らし、最低限の行動だけに絞る。

例：

- X投稿1本だけ
- LINE配信なし
- noteなし
- 今日のログだけ保存
- 次の一手だけ提示

---

## 21. ディレクトリ構成

```text
rts-adapt-engine/
├─ inputs/
│  └─ daily_input.md
├─ prompts/
│  ├─ system.md
│  ├─ normalizer.md
│  ├─ constraint_mapper.md
│  ├─ workflow_planner.md
│  ├─ x_post.md
│  ├─ note.md
│  ├─ line_message.md
│  ├─ line_flow_builder.md
│  ├─ platform_adapter.md
│  ├─ video_script.md
│  ├─ sales_copy.md
│  └─ review.md
├─ configs/
│  ├─ platforms.yaml
│  ├─ publishing_policy.yaml
│  └─ api_budget.yaml
├─ outputs/
│  ├─ context_summary.md
│  ├─ constraint_map.md
│  ├─ workflow_plan.md
│  ├─ x_posts.md
│  ├─ threads_posts.md
│  ├─ bluesky_posts.md
│  ├─ mastodon_posts.md
│  ├─ note_draft.md
│  ├─ line_message.md
│  ├─ video_script.md
│  ├─ sales_copy.md
│  ├─ product_offer.md
│  ├─ dev_log.md
│  ├─ review_checklist.md
│  ├─ summary.md
│  └─ line_flow/
│     ├─ line_flow_spec.md
│     ├─ rich_menu_spec.md
│     ├─ auto_reply_spec.md
│     ├─ quick_reply_spec.md
│     ├─ welcome_message.md
│     ├─ delivery_sequence.md
│     ├─ freebie_delivery.md
│     ├─ consultation_flow.md
│     ├─ product_flow.md
│     └─ faq_reply_spec.md
├─ logs/
│  ├─ execution_log.jsonl
│  ├─ approval_log.jsonl
│  └─ api_call_log.jsonl
├─ rts/
│  ├─ sessions/
│  ├─ manifests/
│  └─ reconstruction.md
├─ src/
│  ├─ generate.py
│  ├─ normalizer.py
│  ├─ planner.py
│  ├─ generators/
│  ├─ line_flow/
│  ├─ adapters/
│  ├─ review/
│  ├─ logging/
│  └─ connectors/
├─ tests/
├─ sample_inputs/
├─ sample_outputs/
├─ README.md
└─ pyproject.toml
```

---

## 22. CLI仕様

v0.1ではCLIで実行する。

### 基本コマンド

```bash
python src/generate.py
```

### 将来コマンド

```text
rts-adapt generate
rts-adapt review
rts-adapt approve
rts-adapt line-flow
rts-adapt export
```

---

## 23. v0.1実装範囲

最初に作るのは以下だけ。

### 入力

```text
inputs/daily_input.md
```

### 出力

```text
outputs/context_summary.md
outputs/x_posts.md
outputs/note_draft.md
outputs/line_message.md
outputs/video_script.md
outputs/review_checklist.md
outputs/summary.md
logs/execution_log.jsonl
```

### v0.1でやらないこと

- LINE公式API連携
- X自動投稿
- Threads自動投稿
- Bluesky自動投稿
- Mastodon自動投稿
- note自動投稿
- 動画生成
- 音声生成
- DB
- Web UI
- 認証
- 課金
- 自動返信
- 完全自動配信

---

## 24. v0.1.5実装範囲

LINE公式の外箱設計を追加する。

```text
outputs/line_flow/
├─ line_flow_spec.md
├─ rich_menu_spec.md
├─ auto_reply_spec.md
├─ welcome_message.md
├─ delivery_sequence.md
└─ consultation_flow.md
```

この段階でもAPI連携はしない。
手動設定用の仕様書を生成する。

---

## 25. v0.2実装範囲

SNS / Platform Extensibility Layer を強化する。

- Canonical Content Model
- Platform Adapter
- Capability Matrix
- platforms.yaml
- 各SNS向けMarkdown出力
- 手動投稿用エクスポート

---

## 26. v0.3実装範囲

RTSログ・承認フローを強化する。

- approval_log.jsonl
- 承認ステータス管理
- RTS用session生成
- decision_log生成
- 出力物の再構成メモ
- 生成物の採用・却下記録

---

## 27. v0.4実装範囲

コネクタを追加する。

優先順位は以下。

1. Markdown Connector
2. GitHub Connector
3. Google Drive Connector
4. LINE手動設定エクスポート
5. note下書き支援
6. X投稿支援
7. Threads / Bluesky / Mastodon投稿支援
8. LINE API Connector

---

## 28. v1.0目標

v1.0では、RTS Adapt Engine が以下を実現する。

- 1つの入力から複数媒体の成果物を生成できる
- LINE公式の外箱仕様を生成できる
- 新規SNSを後から追加できる
- 人間が確認すべきポイントを抽出できる
- 承認ログを残せる
- APIを過剰に叩かない
- RTSに再構成可能な形で記録できる
- コネクタを追加できる構造になっている
- 発信・営業・LINE導線・開発ログに横展開できる

---

## 29. 非目標

RTS Adapt Engine は以下を目指さない。

- バズの保証
- 完全自動SNS運用
- 完全自動営業
- 完全自動LINE運用
- 人間の責任をAIに移すこと
- 法的判断の自動化
- 医療・法律・金融判断の代行
- 炎上リスクゼロの保証
- 全媒体への即時完全対応
- API制限を回避すること
- 複数アカウントで同一内容を大量投稿すること
- 自動いいね・自動フォロー・自動DMを行うこと

---

## 30. 成功条件

### v0.1成功条件

- daily_input.md から複数のMarkdown出力が生成される
- X投稿案が3本以上出る
- note下書きが出る
- LINE配信文が出る
- 動画台本が出る
- review_checklist が出る
- execution_log が残る

### v0.1.5成功条件

- LINE公式の外箱仕様が出る
- リッチメニュー案が出る
- ボタン別応答案が出る
- 登録直後メッセージが出る
- 無料配布導線が出る
- 相談導線が出る

### v0.2成功条件

- 共通コンテンツ形式が定義される
- X / Threads / Bluesky / Mastodon / note / LINE への手動出力が可能になる
- platforms.yaml で媒体ごとの対応状況を管理できる
- 新規SNSを追加してもCore Engineが壊れない

### v1.0成功条件

- 実際の発信・LINE運用・商品導線に使える
- 人間のゼロから作る負荷が下がる
- 人間が確認すべき場所が明確になる
- RTS-AGEの実戦テストケースとして使える
- 開発ログがRTS側に戻る

---

## 31. RTS-AGEとの関係

RTS Adapt Engine は、RTS-AGEの最初の実戦投入先として扱う。

RTS-AGEは本仕様を読み込み、以下を行う。

- 仕様理解
- 計画作成
- タスク分解
- 実装順序決定
- ファイル構成作成
- MVP実装
- smoke test
- 実行ログ保存
- 失敗点抽出
- 改善案生成

RTS Adapt Engine の開発過程そのものを、RTS-AGEの改善材料とする。

---

## 32. 開発方針

全部を一気に作らない。

以下の順で実装する。

1. Markdown入力 → Markdown出力
2. review_checklist生成
3. execution_log保存
4. LINE外箱仕様生成
5. Canonical Content Model追加
6. SNS Platform Adapter追加
7. approval_log追加
8. RTS連携
9. GitHub保存
10. 外部コネクタ
11. LINE API連携
12. 自動化拡張

---

## 33. 仕様凍結ルール

本仕様書 v0.2 Fixed を、RTS Adapt Engine の上位仕様として一旦固定する。

今後の変更は、直接仕様を書き換えるのではなく、以下の形式で管理する。

```text
change_requests/
├─ CR-001.md
├─ CR-002.md
└─ CR-003.md
```

各Change Requestには以下を記録する。

- 変更理由
- 追加したい機能
- 影響範囲
- v0.1に入れるか
- 将来拡張に回すか
- 採用 / 却下 / 保留

これにより、仕様の肥大化を防ぎ、実装範囲を管理する。

---

## 34. 最重要原則

RTS Adapt Engine は、作業を完全に自動化するためのものではない。

目的は、人間がゼロから考え、全部作り、全部確認し、全部継続する状態をやめることである。

AIが準備する。
AIが整理する。
AIが候補を出す。
AIが確認ポイントを出す。
人間は、最後に見る。選ぶ。直す。出す。責任を持つ。

これにより、人間性能に頼り切らないプロジェクト運用を実現する。

# Google API（GA4 & GSC）セットアップガイド

Tokyo Weekender SEO Dashboard に Google Analytics 4 と Google Search Console のデータを接続する手順です。

## 目次

1. [Google Cloud Console の設定](#1-google-cloud-console-の設定)
2. [OAuth 2.0 クライアント ID の作成](#2-oauth-20-クライアント-id-の作成)
3. [API の有効化](#3-api-の有効化)
4. [環境変数の設定](#4-環境変数の設定)
5. [認証情報ファイルの配置](#5-認証情報ファイルの配置)
6. [アプリケーションでの接続](#6-アプリケーションでの接続)
7. [トラブルシューティング](#7-トラブルシューティング)

---

## 1. Google Cloud Console の設定

### 1.1 プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成（または既存のプロジェクトを選択）
   - プロジェクト名: `Tokyo Weekender SEO Dashboard`（任意）

### 1.2 OAuth 同意画面の設定

1. 左メニュー → **API とサービス** → **OAuth 同意画面**
2. ユーザータイプを選択:
   - **外部**: Tokyo Weekender のチームメンバーのみ使用する場合でも外部を選択
3. アプリ情報を入力:
   - **アプリ名**: Tokyo Weekender SEO Dashboard
   - **ユーザーサポートメール**: あなたのメールアドレス
   - **デベロッパーの連絡先情報**: あなたのメールアドレス
4. **保存して次へ**

### 1.3 スコープの設定

1. **スコープを追加または削除** をクリック
2. **この手順はスキップしても OK です**
   - スコープは、アプリケーション側（コード）で自動的に要求されます
   - 必要に応じて後から追加できます
3. **保存して次へ** をクリック

**補足**: 以下のスコープが使用されます（コードで自動的に要求）:
- `https://www.googleapis.com/auth/analytics.readonly` (Google Analytics 4)
- `https://www.googleapis.com/auth/webmasters.readonly` (Google Search Console)

もしスコープを手動で追加したい場合:
1. 「スコープを追加または削除」画面で下にスクロール
2. 「スコープを手動で追加」のテキストボックスに上記 URL を 1 行ずつ貼り付け
3. 「テーブルに追加」をクリック

### 1.4 テストユーザーの追加

1. **テストユーザーを追加** をクリック
2. Tokyo Weekender の GA4 と GSC にアクセス権を持つユーザーのメールアドレスを追加
3. **保存して次へ**

---

## 2. OAuth 2.0 クライアント ID の作成

### 2.1 クライアント ID の作成

1. 左メニュー → **API とサービス** → **認証情報**
2. **認証情報を作成** → **OAuth クライアント ID**
3. アプリケーションの種類: **ウェブ アプリケーション**
4. 名前: `Tokyo Weekender Dashboard Client`（任意）
5. **承認済みのリダイレクト URI** を追加:
   - 開発環境: `http://localhost:5173/settings`
   - 本番環境: `https://your-production-domain.com/settings`
6. **作成** をクリック
7. ポップアップダイアログが表示されます（クライアント ID とシークレットが表示される）
   - ダイアログは **一旦閉じて OK** です

### 2.2 クライアントシークレット JSON のダウンロード

1. **API とサービス** → **認証情報** ページに戻る
2. **OAuth 2.0 クライアント ID** セクションで、先ほど作成した「Tokyo Weekender Dashboard Client」を探す
3. 右側の **ダウンロードアイコン**（↓ マーク）をクリック
   - または、クライアント ID の名前をクリックして詳細ページを開き、右上の **JSON をダウンロード** をクリック
4. ファイル名は `client_secret_xxxxx.apps.googleusercontent.com.json` のような形式でダウンロードされます

---

## 3. API の有効化

### 3.1 Google Analytics Data API の有効化

1. 左メニュー → **API とサービス** → **ライブラリ**
2. 「Google Analytics Data API」を検索
3. **有効にする** をクリック

### 3.2 Google Search Console API の有効化

1. 左メニュー → **API とサービス** → **ライブラリ**
2. 「Google Search Console API」を検索
3. **有効にする** をクリック

---

## 4. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成（または既存ファイルに追加）:

```bash
# Google API Configuration
# GA4 Property ID を設定（GA4 管理画面から取得）
GA4_PROPERTY_ID=123456789

# GSC Site URL を設定
GSC_SITE_URL=https://www.tokyoweekender.com/

# Google OAuth 2.0 リダイレクト URI
# 開発環境
GOOGLE_REDIRECT_URI=http://localhost:5173/settings

# 本番環境（デプロイ時に変更）
# GOOGLE_REDIRECT_URI=https://your-production-domain.com/settings
```

### GA4 Property ID の取得方法

1. [Google Analytics](https://analytics.google.com/) にアクセス
2. Tokyo Weekender のプロパティを選択
3. 左下の **管理** → **プロパティ設定**
4. 「プロパティ ID」をコピー（例: 123456789）

---

## 5. 認証情報ファイルの配置

### 5.1 ダウンロードしたファイルの確認

ダウンロードした JSON ファイルは以下のような名前になっています：
- `client_secret_xxxxx.apps.googleusercontent.com.json`

### 5.2 ファイルの配置

1. プロジェクトルートで認証情報ディレクトリを作成:

```bash
mkdir -p data/credentials
```

2. ダウンロードした JSON ファイルを配置（ファイル名を変更）:

```bash
# Downloads フォルダからコピー
cp ~/Downloads/client_secret_*.apps.googleusercontent.com.json data/credentials/google_client_secret.json
```

または、手動でファイルをコピー:
- ダウンロードフォルダから `client_secret_xxxxx.apps.googleusercontent.com.json` をコピー
- `data/credentials/` フォルダに貼り付け
- ファイル名を `google_client_secret.json` に変更

3. 最終的なファイルパス:

```
tokyo-weekender/
  └── data/
      └── credentials/
          └── google_client_secret.json  ← このファイル名にする
```

### 5.3 セキュリティ確認

`.gitignore` に追加されていることを確認（重要！）:

```bash
# .gitignore に以下が含まれていることを確認
cat .gitignore | grep "data/credentials"
```

**重要**: この JSON ファイルは絶対に Git にコミットしないでください！

---

## 6. アプリケーションでの接続

### 6.1 依存関係のインストール

```bash
# Backend の依存関係をインストール
pip install -r requirements.txt
```

### 6.2 Backend の起動

```bash
# プロジェクトルートから
cd backend
python main.py

# または uvicorn を直接使用
uvicorn backend.main:app --reload --port 8000
```

### 6.3 Frontend の起動

```bash
# 別のターミナルで
cd frontend
npm install
npm run dev
```

### 6.4 Google アカウントに接続

1. ブラウザで `http://localhost:5173` を開く
2. 左メニューから **Settings** をクリック
3. **Google API 接続** セクションで **Google アカウントに接続** ボタンをクリック
4. ポップアップウィンドウで Google アカウントにログイン
5. Tokyo Weekender の GA4 と GSC にアクセス権があるアカウントでログイン
6. アクセス許可を確認して **許可** をクリック
7. ポップアップが閉じたら、接続ステータスが「接続済み」になることを確認

### 6.5 データの確認

接続後、以下のエンドポイントでデータを取得できます:

#### GA4 データ

- リアルタイムデータ: `GET /api/ga4/realtime`
- トラフィック概要: `GET /api/ga4/overview?start_date=2024-09-01&end_date=2024-09-30`
- トラフィックソース: `GET /api/ga4/sources?start_date=2024-09-01&end_date=2024-09-30`
- 人気ページ: `GET /api/ga4/pages?start_date=2024-09-01&end_date=2024-09-30`
- 日別トラフィック: `GET /api/ga4/daily?start_date=2024-09-01&end_date=2024-09-30`
- 国別トラフィック: `GET /api/ga4/countries?start_date=2024-09-01&end_date=2024-09-30`
- デバイス別トラフィック: `GET /api/ga4/devices?start_date=2024-09-01&end_date=2024-09-30`
- オーガニック検索トラフィック: `GET /api/ga4/organic?start_date=2024-09-01&end_date=2024-09-30`

#### GSC データ

- 検索パフォーマンス概要: `GET /api/gsc/overview?start_date=2024-09-01&end_date=2024-09-30`
- 上位検索クエリ: `GET /api/gsc/queries?start_date=2024-09-01&end_date=2024-09-30`
- 上位ページ: `GET /api/gsc/pages?start_date=2024-09-01&end_date=2024-09-30`
- 国別パフォーマンス: `GET /api/gsc/countries?start_date=2024-09-01&end_date=2024-09-30`
- デバイス別パフォーマンス: `GET /api/gsc/devices?start_date=2024-09-01&end_date=2024-09-30`
- 日別パフォーマンス: `GET /api/gsc/daily?start_date=2024-09-01&end_date=2024-09-30`
- 特定ページのパフォーマンス: `GET /api/gsc/page-performance?page_url=https://www.tokyoweekender.com/example`
- 特定クエリのパフォーマンス: `GET /api/gsc/query-performance?query=tokyo events`

---

## 7. トラブルシューティング

### 問題: OAuth クライアント ID 作成後に JSON ダウンロードボタンが見つからない

**解決策:**
1. **API とサービス** → **認証情報** ページを開く
2. 「**OAuth 2.0 クライアント ID**」セクションを確認
3. 作成したクライアント ID の**右側にあるダウンロードアイコン（↓）** をクリック
4. またはクライアント ID の名前をクリックして、右上の「**JSON をダウンロード**」をクリック

**補足:**
- 作成完了時のダイアログは閉じても OK です
- JSON ファイルはいつでも認証情報ページから再ダウンロード可能です

### 問題: 「クライアントシークレットファイルが見つかりません」エラー

**解決策:**
- `data/credentials/google_client_secret.json` ファイルが存在することを確認
- ファイル名が正確に一致していることを確認（`client_secret_xxx.json` ではなく `google_client_secret.json`）
- ファイルのパーミッションを確認
- JSON ファイルの内容が正しい形式かを確認（有効な JSON）

```bash
# ファイルの存在確認
ls -la data/credentials/google_client_secret.json

# JSON の形式確認
cat data/credentials/google_client_secret.json | python -m json.tool
```

### 問題: 「認証 URL の生成に失敗」エラー

**解決策:**
- Google Cloud Console で OAuth 同意画面の設定が完了していることを確認
- OAuth 2.0 クライアント ID が正しく作成されていることを確認
- リダイレクト URI が正しく設定されていることを確認

### 問題: 「Google アカウントに接続されていません」エラー

**解決策:**
- Settings ページで再度 Google アカウントに接続
- トークンファイル（`data/credentials/google_token.json`）を削除して再認証

### 問題: 「GA4_PROPERTY_ID が環境変数に設定されていません」エラー

**解決策:**
- `.env` ファイルに `GA4_PROPERTY_ID` が設定されていることを確認
- Backend を再起動して環境変数を読み込み直す

### 問題: GSC データが取得できない

**解決策:**
- GSC でサイトの所有権が確認されていることを確認
- 接続したアカウントが GSC で Tokyo Weekender サイトへのアクセス権を持っていることを確認
- `GSC_SITE_URL` が正しく設定されていることを確認（末尾のスラッシュを含む）

### 問題: ポップアップがブロックされる

**解決策:**
- ブラウザのポップアップブロッカーを無効化
- または、ポップアップ許可のダイアログで「許可」を選択

### 問題: トークンが期限切れになる

**説明:**
- OAuth トークンは一定期間で期限切れになります
- アプリケーションは自動的にトークンをリフレッシュしますが、リフレッシュトークンが無効になった場合は再認証が必要です

**解決策:**
- Settings ページで「接続解除」→「Google アカウントに接続」を実行して再認証

---

## セキュリティに関する注意事項

1. **認証情報ファイルは絶対に Git にコミットしない**
   - `data/credentials/` ディレクトリは `.gitignore` に追加済み
   
2. **本番環境では適切な権限管理を行う**
   - ファイルのパーミッションを制限（例: `chmod 600 data/credentials/*.json`）
   
3. **リダイレクト URI は本番環境のドメインのみに制限**
   - Google Cloud Console で承認済みリダイレクト URI を適切に設定

4. **定期的にアクセス権を確認**
   - Google Cloud Console → 認証情報 → OAuth 2.0 クライアント ID
   - 不要なリダイレクト URI は削除

---

## 本番環境へのデプロイ

### 環境変数の設定

本番環境（Render など）で以下の環境変数を設定:

```bash
GA4_PROPERTY_ID=your-actual-property-id
GSC_SITE_URL=https://www.tokyoweekender.com/
GOOGLE_REDIRECT_URI=https://your-production-domain.com/settings
```

### クライアントシークレットファイル

1. Render の環境変数として設定する方法:
   - ファイルの内容を環境変数 `GOOGLE_CLIENT_SECRET_JSON` として設定
   - Backend 起動時に環境変数から JSON ファイルを生成

2. または、Render のストレージに直接アップロード

### リダイレクト URI の更新

Google Cloud Console で本番環境のリダイレクト URI を追加:

```
https://your-production-domain.com/settings
```

---

## 参考リンク

- [Google Analytics Data API Documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Google Search Console API Documentation](https://developers.google.com/webmaster-tools)
- [OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)

---

## サポート

問題が解決しない場合は、以下を確認してください:

1. Backend のログ（ターミナル出力）
2. Frontend のコンソール（ブラウザのデベロッパーツール）
3. Google Cloud Console のログ


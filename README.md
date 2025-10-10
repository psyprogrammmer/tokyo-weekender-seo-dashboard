# Tokyo Weekender Organic Growth Analysis Dashboard

Tokyo WeekenderのOrganic Growthを促進するための包括的な分析基盤とコンテンツ戦略提案ダッシュボードです。

## 機能

### 1. Tokyo Weekender 現状分析
- キーワードパフォーマンス分析
- トラフィックトレンド分析
- SERP機能の取得状況
- コンテンツ意図別分析

### 2. 競合サイト分析
- 競合とのキーワード比較
- 機会分析（競合が上位だがTokyo Weekenderが未取得のキーワード）
- 競合の強み・弱み分析

### 3. 新規コンテンツ制作提案
- 高ボリューム・低競合キーワードの発見
- コンテンツギャップ分析
- トピッククラスター提案

### 4. 既存コンテンツ改善提案
- 順位改善の可能性が高いキーワード
- コンテンツ最適化提案
- 内部リンク戦略

## データソース

- Tokyo Weekender キーワードリスト（Ahrefs）
- **Google Analytics 4** (GA4) - リアルタイムトラフィックデータ
- **Google Search Console** (GSC) - 検索パフォーマンスデータ
- 競合サイトキーワードリスト（Ahrefs）

## 技術スタック

### バックエンド
- Python 3.11+
- FastAPI
- **NEON PostgreSQL** (Serverless PostgreSQL)
- SQLAlchemy with Alembic
- Pandas, NumPy
- scikit-learn
- **Google Analytics Data API** - GA4 データ取得
- **Google Search Console API** - GSC データ取得
- Google OAuth 2.0 認証

### フロントエンド
- React 18
- TypeScript
- Tailwind CSS
- Chart.js
- D3.js

## セットアップ

### 1. NEON データベースの設定

詳細な設定手順は [NEON_SETUP.md](docs/NEON_SETUP.md) を参照してください。

1. [NEON](https://neon.tech/) でアカウント作成
2. プロジェクト作成とデータベース接続情報の取得
3. `.env` ファイルの設定

```bash
# 環境設定ファイルのコピー
cp env.example .env
# .env ファイルを編集してNEONの接続情報を設定
```

### 2. 依存関係のインストール

```bash
# バックエンド依存関係
pip install -r requirements.txt

# フロントエンド依存関係
npm install
```

### 3. Google API の設定（オプション）

GA4 と GSC のリアルタイムデータを取得する場合、Google API の設定が必要です。

詳細な設定手順は [GOOGLE_API_SETUP.md](docs/GOOGLE_API_SETUP.md) を参照してください。

簡易手順:
1. Google Cloud Console で OAuth 2.0 クライアント ID を作成
2. クライアントシークレット JSON を `data/credentials/google_client_secret.json` に配置
3. `.env` に GA4 Property ID と GSC Site URL を設定
4. アプリケーションの Settings ページで Google アカウントに接続

### 4. データベースの初期化

```bash
# データベースマイグレーション
alembic upgrade head

# CSVデータをNEONデータベースに移行
python analysis/scripts/migrate_to_neon.py
```

### 5. アプリケーションの起動

```bash
# バックエンド起動
cd backend && python main.py

# フロントエンド起動（別ターミナル）
npm run dev
```

## データ構造

### キーワードデータ
- Keyword: キーワード
- Volume: 月間検索ボリューム
- KD: キーワード難易度
- CPC: クリック単価
- Organic traffic: オーガニックトラフィック
- Current position: 現在の順位
- Current URL: 対象URL
- SERP features: SERP機能
- 意図分類: Navigational, Informational, Commercial, Transactional, Branded, Local

## プロジェクト構造

```
tokyo-weekender/
├── backend/           # FastAPI バックエンド
│   ├── models/       # SQLAlchemy データベースモデル
│   └── services/     # データベースサービス
├── frontend/          # React フロントエンド
├── data/             # データファイル
├── analysis/         # 分析スクリプト
├── migrations/       # Alembic マイグレーション
└── docs/            # ドキュメント
```

## NEON データベース統合の利点

### 🚀 パフォーマンス向上
- **Serverless PostgreSQL**: 自動スケーリングとコールドスタート最適化
- **高速クエリ**: インデックス最適化による高速データアクセス
- **接続プーリング**: 効率的なデータベース接続管理

### 📊 データ管理の改善
- **構造化データ**: SQLAlchemyモデルによる型安全なデータ操作
- **マイグレーション**: Alembicによるスキーマ変更管理
- **バックアップ**: 自動バックアップとポイントインタイム復旧

### 🔄 リアルタイム分析
- **即座のクエリ**: データベースからの直接分析結果取得
- **フィルタリング**: 高度な検索とフィルタリング機能
- **集計処理**: SQL による効率的なデータ集計

## Google API 統合（新機能）

### ✅ 実装済み機能

#### Google Analytics 4 (GA4)
- **リアルタイムデータ**: 現在のアクティブユーザー数と所在地
- **トラフィック概要**: セッション数、ユーザー数、ページビュー数、直帰率など
- **トラフィックソース**: チャネル別のトラフィック分析
- **人気ページ**: ページビュー数が多いページのランキング
- **地域別トラフィック**: 国別・都市別のトラフィック分布
- **デバイス別トラフィック**: デスクトップ・モバイル・タブレット別分析
- **オーガニック検索トラフィック**: 検索エンジン別のオーガニックトラフィック

#### Google Search Console (GSC)
- **検索パフォーマンス概要**: クリック数、表示回数、CTR、平均掲載順位
- **上位検索クエリ**: クリック数が多いクエリのランキング
- **上位ページ**: 検索パフォーマンスが高いページのランキング
- **地域別パフォーマンス**: 国別の検索パフォーマンス
- **デバイス別パフォーマンス**: デバイス別の検索パフォーマンス
- **日別パフォーマンス**: 時系列での検索パフォーマンス推移
- **特定ページ/クエリの分析**: 詳細なページ・クエリ別分析

### 🔐 セキュリティ

- **OAuth 2.0 認証**: Google の標準的な認証フロー
- **スコープ制限**: 読み取り専用アクセス（`.readonly`）
- **トークン管理**: 自動リフレッシュとセキュアな保存

## 今後の拡張予定

1. ✅ ~~**Google Search Console連携**: リアルタイムデータ取得とNEON同期~~ (実装済み)
2. **競合分析の自動化**: 複数競合サイトの比較分析
3. **AI駆動コンテンツ提案**: 機械学習によるコンテンツ戦略提案
4. **レポート自動生成**: 定期的な分析レポートの自動生成
5. **GA4/GSC データの自動同期**: データベースへの定期的なデータ保存
5. **リアルタイムダッシュボード**: WebSocketによるリアルタイム更新

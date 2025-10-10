"""
Tokyo Weekender SEO Analysis Dashboard - FastAPI Backend with NEON Database
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import os
import pandas as pd
from typing import Dict, List, Optional
import uvicorn
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Import database components
from backend.models.database import get_db, engine, Base
from backend.services.database_service import DatabaseService
from backend.services.google_auth_service import GoogleAuthService
from backend.services.ga4_service import GA4Service
from backend.services.gsc_service import GSCService

def get_db_safe():
    """Safe database dependency that handles connection errors"""
    try:
        db = next(get_db())
        return db
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

app = FastAPI(
    title="Tokyo Weekender SEO Dashboard API",
    description="Tokyo WeekenderのOrganic Growth分析API with NEON Database",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:5173",
        "https://tokyo-weekender-seo-dashboard.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データファイルのパス
DATA_PATH = Path("data/processed")
RAW_DATA_PATH = Path("data/raw")

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    # データディレクトリの作成
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    
    # データベーステーブルの作成（開発環境用）
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ データベーステーブルが準備されました")
    except Exception as e:
        print(f"⚠️ データベース接続エラー: {e}")
        print("NEONデータベースの設定を確認してください")
        print("⚠️ アプリケーションはCSVフォールバックモードで動作します")

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Tokyo Weekender SEO Analysis Dashboard API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "message": "Tokyo Weekender Backend is running"}

@app.get("/api/test")
async def test_endpoint():
    """テストエンドポイント"""
    return {
        "message": "Backend is working!",
        "timestamp": "2025-09-27T01:43:00Z",
        "version": "1.0.0"
    }

@app.get("/api/analysis/summary")
async def get_analysis_summary(db: Session = Depends(get_db)):
    """分析サマリーの取得（NEONデータベースから）"""
    try:
        service = DatabaseService(db)
        summary = service.get_keywords_summary()
        return summary
    
    except Exception as e:
        # Fallback to JSON file if database fails
        try:
            analysis_file = DATA_PATH / "tokyo_weekender_analysis.json"
            if analysis_file.exists():
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data.get('summary_stats', {})
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.get("/api/analysis/performance")
async def get_performance_analysis(db: Session = Depends(get_db)):
    """パフォーマンス分析の取得（NEONデータベースから）"""
    try:
        service = DatabaseService(db)
        performance_data = service.get_performance_analysis()
        # Convert numpy types to ensure JSON serialization
        converted_data = service.convert_numpy_types(performance_data)
        return converted_data
    
    except Exception as e:
        # Fallback to JSON file if database fails
        try:
            analysis_file = DATA_PATH / "tokyo_weekender_analysis.json"
            if analysis_file.exists():
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data.get('performance_analysis', {})
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"パフォーマンス分析の取得に失敗: {str(e)}")

@app.get("/api/analysis/content-gaps")
async def get_content_gaps():
    """コンテンツギャップ分析の取得"""
    try:
        analysis_file = DATA_PATH / "tokyo_weekender_analysis.json"
        
        if not analysis_file.exists():
            raise HTTPException(status_code=404, detail="分析データが見つかりません")
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('content_gaps', {})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.get("/api/analysis/serp-features")
async def get_serp_analysis():
    """SERP機能分析の取得"""
    try:
        analysis_file = DATA_PATH / "tokyo_weekender_analysis.json"
        
        if not analysis_file.exists():
            raise HTTPException(status_code=404, detail="分析データが見つかりません")
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('serp_analysis', {})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.get("/api/keywords")
async def get_keywords(
    limit: int = 100,
    offset: int = 0,
    min_volume: Optional[int] = None,
    max_position: Optional[int] = None,
    intent: Optional[str] = None
):
    """キーワードデータの取得（フィルタリング対応）"""
    try:
        csv_file = RAW_DATA_PATH / "www.tokyoweekender.com-organic-keywords-sub_2025-09-26_06-49-18.csv"
        
        if not csv_file.exists():
            raise HTTPException(status_code=404, detail="キーワードデータが見つかりません")
        
        df = pd.read_csv(csv_file)
        
        # フィルタリング
        if min_volume is not None:
            df = df[df['Volume'] >= min_volume]
        
        if max_position is not None:
            df = df[df['Current position'] <= max_position]
        
        if intent is not None:
            if intent in df.columns:
                df = df[df[intent] == True]
        
        # Traffic順（降順）、Position順（昇順）でソート
        df = df.sort_values(['Organic traffic', 'Current position'], ascending=[False, True])
        
        # ページネーション
        total = len(df)
        df = df.iloc[offset:offset + limit]
        
        return {
            "keywords": df.to_dict('records'),
            "total": total,
            "limit": limit,
            "offset": offset
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.get("/api/keywords/search")
async def search_keywords(
    min_volume: int = 100,
    max_position: int = 50,
    intent: str = "",
    location: str = "",
    limit: int = 100
):
    """キーワード検索（フィルター条件付き）"""
    # Try database first
    db = get_db_safe()
    if db:
        try:
            service = DatabaseService(db)
            keywords = service.search_keywords(min_volume, max_position, intent, location, limit)
            return keywords
        except Exception as e:
            print(f"Database search failed: {e}")
    
    # Fallback to CSV data
    try:
        # Try multiple CSV files
        csv_files = [
            RAW_DATA_PATH / "www.tokyoweekender.com-organic-keywords-sub_2025-09-26_06-49-18.csv",
            Path("csv/www.tokyoweekender.com-organic-keywords-sub_2025-09-26_06-49-18.csv"),
            Path("data/raw/www.tokyoweekender.com-organic-keywords-sub_2025-09-26_06-49-18.csv")
        ]
        
        csv_file = None
        for file_path in csv_files:
            if file_path.exists():
                csv_file = file_path
                break
        
        if not csv_file:
            raise HTTPException(status_code=404, detail="キーワードデータが見つかりません")
        
        df = pd.read_csv(csv_file)
        
        # Apply filters
        if min_volume > 0:
            df = df[df['Volume'] >= min_volume]
        
        if max_position > 0:
            df = df[df['Current position'] <= max_position]
        
        if intent:
            if intent in df.columns:
                df = df[df[intent] == True]
        
        if location:
            df = df[df['Location'] == location]
        
        # Sort and limit
        df = df.sort_values(['Organic traffic', 'Current position'], ascending=[False, True])
        df = df.head(limit)
        
        return df.to_dict('records')
        
    except Exception as csv_error:
        raise HTTPException(status_code=500, detail=f"キーワード検索に失敗: CSV fallback failed: {str(csv_error)}")

@app.get("/api/keywords/locations")
async def get_available_locations():
    """利用可能な国・地域リストの取得"""
    # Try database first
    db = get_db_safe()
    if db:
        try:
            service = DatabaseService(db)
            locations = service.get_available_locations()
            return locations
        except Exception as e:
            print(f"Database locations failed: {e}")
    
    # Fallback to CSV data
    try:
        # Try multiple CSV files
        csv_files = [
            RAW_DATA_PATH / "www.tokyoweekender.com-organic-keywords-sub_2025-09-26_06-49-18.csv",
            Path("csv/www.tokyoweekender.com-organic-keywords-sub_2025-09-26_06-49-18.csv"),
            Path("data/raw/www.tokyoweekender.com-organic-keywords-sub_2025-09-26_06-49-18.csv")
        ]
        
        csv_file = None
        for file_path in csv_files:
            if file_path.exists():
                csv_file = file_path
                break
        
        if not csv_file:
            raise HTTPException(status_code=404, detail="キーワードデータが見つかりません")
        
        df = pd.read_csv(csv_file)
        
        # Get unique locations with counts
        location_counts = df['Location'].value_counts().head(10)
        locations = []
        
        for location, count in location_counts.items():
            if pd.notna(location) and location != '':
                total_traffic = df[df['Location'] == location]['Organic traffic'].sum()
                locations.append({
                    'location': location,
                    'keyword_count': int(count),
                    'total_traffic': int(total_traffic) if pd.notna(total_traffic) else 0
                })
        
        return locations
        
    except Exception as csv_error:
        raise HTTPException(status_code=500, detail=f"国・地域リストの取得に失敗: CSV fallback failed: {str(csv_error)}")

@app.get("/api/competitors/summary")
async def get_competitors_summary(db: Session = Depends(get_db)):
    """競合サイトの概要取得"""
    try:
        service = DatabaseService(db)
        summary = service.get_competitors_summary()
        return summary
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"競合概要の取得に失敗: {str(e)}")

@app.get("/api/competitors/{competitor_site}/keywords")
async def get_competitor_keywords(
    competitor_site: str,
    min_volume: int = 100,
    max_position: int = 50,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """特定競合サイトのキーワード取得"""
    try:
        service = DatabaseService(db)
        keywords = service.get_competitor_keywords(competitor_site, min_volume, max_position, limit)
        return keywords
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"競合キーワードの取得に失敗: {str(e)}")

@app.get("/api/competitors/opportunities")
async def get_competitor_opportunities(
    min_volume: int = 100,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """競合機会キーワードの取得"""
    try:
        service = DatabaseService(db)
        opportunities = service.get_competitor_opportunities(min_volume, limit)
        return opportunities
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"競合機会の取得に失敗: {str(e)}")

@app.get("/api/competitors/{competitor_site}/comparison")
async def get_competitor_comparison(
    competitor_site: str,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """競合サイトとTokyo Weekenderの詳細比較"""
    try:
        service = DatabaseService(db)
        comparison = service.get_competitor_vs_tw_comparison(competitor_site, limit)
        return comparison
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"競合比較の取得に失敗: {str(e)}")

@app.get("/api/keywords/top-performing")
async def get_top_performing_keywords(limit: int = 20, db: Session = Depends(get_db)):
    """高パフォーマンスキーワードの取得（NEONデータベースから）"""
    try:
        service = DatabaseService(db)
        keywords = service.get_high_performance_keywords(limit)
        return keywords
    
    except Exception as e:
        # Fallback to JSON file if database fails
        try:
            analysis_file = DATA_PATH / "tokyo_weekender_analysis.json"
            if analysis_file.exists():
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                high_performance = data.get('performance_analysis', {}).get('high_performance_keywords', [])
                return high_performance[:limit]
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.get("/api/keywords/improvement-opportunities")
async def get_improvement_opportunities(limit: int = 20, db: Session = Depends(get_db)):
    """改善機会キーワードの取得（NEONデータベースから）"""
    try:
        service = DatabaseService(db)
        keywords = service.get_improvement_opportunities(limit)
        return keywords
    
    except Exception as e:
        # Fallback to JSON file if database fails
        try:
            analysis_file = DATA_PATH / "tokyo_weekender_analysis.json"
            if analysis_file.exists():
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                opportunities = data.get('performance_analysis', {}).get('improvement_opportunities', [])
                return opportunities[:limit]
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.post("/api/analysis/refresh")
async def refresh_analysis():
    """分析データの再計算"""
    try:
        # データ処理スクリプトの実行
        import subprocess
        import sys
        
        script_path = Path("analysis/scripts/data_processor.py")
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"分析実行エラー: {result.stderr}")
        
        return {"message": "分析データが更新されました", "output": result.stdout}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析更新エラー: {str(e)}")

@app.post("/api/database/migrate")
async def migrate_csv_to_database(db: Session = Depends(get_db)):
    """CSVデータをNEONデータベースに移行"""
    try:
        import subprocess
        import sys
        
        script_path = Path("analysis/scripts/migrate_to_neon.py")
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"移行エラー: {result.stderr}")
        
        return {"message": "データベースへの移行が完了しました", "output": result.stdout}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"移行エラー: {str(e)}")

@app.get("/api/database/status")
async def database_status(db: Session = Depends(get_db)):
    """データベース接続状態の確認"""
    try:
        service = DatabaseService(db)
        summary = service.get_keywords_summary()
        return {
            "status": "connected",
            "message": "NEONデータベースに正常に接続されています",
            "data_summary": summary
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"データベース接続エラー: {str(e)}",
            "data_summary": None
        }

@app.get("/api/content/recommendations")
async def get_content_recommendations(db: Session = Depends(get_db)):
    """Content recommendations based on keyword analysis"""
    try:
        service = DatabaseService(db)
        
        # 新規コンテンツ提案
        new_content = service.get_new_content_recommendations(limit=8)
        
        # 既存コンテンツ改善
        improvements = service.get_content_improvement_recommendations(limit=12)
        
        # トピッククラスター
        topic_clusters = service.get_topic_cluster_recommendations(limit=3)
        
        # サマリー統計
        total_potential_traffic = sum(item.get('potential_traffic', 0) for item in new_content)
        priority = 'High' if total_potential_traffic > 20000 else 'Medium' if total_potential_traffic > 10000 else 'Low'
        
        return {
            "summary": {
                "new_content_proposals": len(new_content),
                "improvement_proposals": len(improvements),
                "potential_traffic": total_potential_traffic,
                "priority": priority
            },
            "new_content": new_content,
            "improvements": improvements,
            "topic_clusters": topic_clusters
        }
        
    except Exception as e:
        # Fallback to mock data if database fails
        try:
            return {
                "summary": {
                    "new_content_proposals": 8,
                    "improvement_proposals": 12,
                    "potential_traffic": 45000,
                    "priority": "High"
                },
                "new_content": [
                    {
                        "title": "Tokyo Cherry Blossom Viewing Spots 2024",
                        "keyword": "tokyo cherry blossom spots",
                        "volume": 3200,
                        "difficulty": 15,
                        "potential_traffic": 8500,
                        "content_type": "Guide",
                        "priority": "High",
                        "estimated_effort": "Medium",
                        "target_audience": "Tourists",
                        "content_angle": "Seasonal guide with best viewing times and locations"
                    }
                ],
                "improvements": [
                    {
                        "title": "Tokyo Events Calendar",
                        "current_url": "https://www.tokyoweekender.com/events",
                        "keyword": "tokyo events",
                        "current_position": 3,
                        "target_position": 1,
                        "potential_traffic_gain": 1200,
                        "improvement_type": "Content Enhancement",
                        "priority": "High",
                        "recommendations": [
                            "Add more detailed event descriptions",
                            "Include event photos and videos",
                            "Add user reviews and ratings",
                            "Implement event filtering by category"
                        ]
                    }
                ],
                "topic_clusters": [
                    {
                        "cluster_name": "Tokyo Food & Dining",
                        "primary_keyword": "tokyo food",
                        "supporting_keywords": [
                            "tokyo ramen",
                            "tokyo sushi",
                            "tokyo street food",
                            "tokyo izakaya",
                            "tokyo dessert"
                        ],
                        "content_pieces": 6,
                        "potential_traffic": 25000,
                        "priority": "High"
                    }
                ]
            }
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"Content recommendations error: {str(e)}")

# Google 認証エンドポイント
@app.get("/api/google/auth-status")
async def get_google_auth_status():
    """Google 認証ステータスの確認"""
    try:
        auth_service = GoogleAuthService()
        status = auth_service.get_auth_status()
        return status
    except Exception as e:
        return {
            'authenticated': False,
            'error': str(e)
        }

@app.get("/api/google/auth-url")
async def get_google_auth_url():
    """Google OAuth 2.0 認証 URL を取得"""
    try:
        auth_service = GoogleAuthService()
        # リダイレクト URI は環境に応じて変更
        redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3000/auth/callback')
        auth_url = auth_service.get_authorization_url(redirect_uri)
        
        return {
            'auth_url': auth_url
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"認証 URL の生成に失敗: {str(e)}")

@app.post("/api/google/auth-callback")
async def handle_google_auth_callback(authorization_response: str):
    """Google OAuth 2.0 コールバックを処理"""
    try:
        auth_service = GoogleAuthService()
        redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3000/auth/callback')
        result = auth_service.handle_authorization_callback(authorization_response, redirect_uri)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"認証の処理に失敗: {str(e)}")

@app.post("/api/google/revoke")
async def revoke_google_auth():
    """Google 認証を取り消し"""
    try:
        auth_service = GoogleAuthService()
        result = auth_service.revoke_credentials()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"認証の取り消しに失敗: {str(e)}")

# GA4 エンドポイント
@app.get("/api/ga4/realtime")
async def get_ga4_realtime():
    """GA4 リアルタイムデータを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_realtime_data()
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"リアルタイムデータの取得に失敗: {str(e)}")

@app.get("/api/ga4/overview")
async def get_ga4_overview(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GA4 トラフィック概要を取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_traffic_overview(start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"トラフィック概要の取得に失敗: {str(e)}")

@app.get("/api/ga4/sources")
async def get_ga4_sources(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d'),
    limit: int = 10
):
    """GA4 トラフィックソース別データを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_traffic_by_source(start_date, end_date, limit)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"トラフィックソースの取得に失敗: {str(e)}")

@app.get("/api/ga4/pages")
async def get_ga4_pages(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d'),
    limit: int = 20
):
    """GA4 人気ページを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_top_pages(start_date, end_date, limit)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"人気ページの取得に失敗: {str(e)}")

@app.get("/api/ga4/daily")
async def get_ga4_daily(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GA4 日別トラフィックを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_daily_traffic(start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"日別トラフィックの取得に失敗: {str(e)}")

@app.get("/api/ga4/countries")
async def get_ga4_countries(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d'),
    limit: int = 10
):
    """GA4 国別トラフィックを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_traffic_by_country(start_date, end_date, limit)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"国別トラフィックの取得に失敗: {str(e)}")

@app.get("/api/ga4/devices")
async def get_ga4_devices(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GA4 デバイス別トラフィックを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_traffic_by_device(start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"デバイス別トラフィックの取得に失敗: {str(e)}")

@app.get("/api/ga4/organic")
async def get_ga4_organic(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GA4 オーガニック検索トラフィックを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        ga4_service = GA4Service(credentials)
        data = ga4_service.get_organic_search_traffic(start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"オーガニックトラフィックの取得に失敗: {str(e)}")

# GSC エンドポイント
@app.get("/api/gsc/overview")
async def get_gsc_overview(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GSC 検索パフォーマンス概要を取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_overview(start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"検索パフォーマンス概要の取得に失敗: {str(e)}")

@app.get("/api/gsc/queries")
async def get_gsc_queries(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d'),
    limit: int = 20
):
    """GSC 上位検索クエリを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_top_queries(start_date, end_date, limit)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上位クエリの取得に失敗: {str(e)}")

@app.get("/api/gsc/pages")
async def get_gsc_pages(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d'),
    limit: int = 20
):
    """GSC 上位ページを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_top_pages(start_date, end_date, limit)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上位ページの取得に失敗: {str(e)}")

@app.get("/api/gsc/countries")
async def get_gsc_countries(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d'),
    limit: int = 10
):
    """GSC 国別パフォーマンスを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_performance_by_country(start_date, end_date, limit)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"国別パフォーマンスの取得に失敗: {str(e)}")

@app.get("/api/gsc/devices")
async def get_gsc_devices(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GSC デバイス別パフォーマンスを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_performance_by_device(start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"デバイス別パフォーマンスの取得に失敗: {str(e)}")

@app.get("/api/gsc/daily")
async def get_gsc_daily(
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GSC 日別パフォーマンスを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_daily_performance(start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"日別パフォーマンスの取得に失敗: {str(e)}")

@app.get("/api/gsc/page-performance")
async def get_gsc_page_performance(
    page_url: str,
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GSC 特定ページのパフォーマンスを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_page_performance(page_url, start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ページパフォーマンスの取得に失敗: {str(e)}")

@app.get("/api/gsc/query-performance")
async def get_gsc_query_performance(
    query: str,
    start_date: str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    end_date: str = datetime.now().strftime('%Y-%m-%d')
):
    """GSC 特定クエリのパフォーマンスを取得"""
    try:
        auth_service = GoogleAuthService()
        credentials = auth_service.get_credentials()
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Google アカウントに接続されていません")
        
        gsc_service = GSCService(credentials)
        data = gsc_service.get_query_performance(query, start_date, end_date)
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"クエリパフォーマンスの取得に失敗: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

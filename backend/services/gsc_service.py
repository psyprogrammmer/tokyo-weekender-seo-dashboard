"""
Google Search Console (GSC) データ取得サービス
"""
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv()


class GSCService:
    """Google Search Console データを取得するサービス"""
    
    def __init__(self, credentials: Credentials):
        """
        初期化
        
        Args:
            credentials: Google OAuth 2.0 認証情報
        """
        self.credentials = credentials
        self.service = build('searchconsole', 'v1', credentials=credentials)
        self.site_url = os.getenv('GSC_SITE_URL', 'https://www.tokyoweekender.com/')
        
        # サイト URL が末尾にスラッシュを持つことを確認
        if not self.site_url.endswith('/'):
            self.site_url += '/'
    
    def get_search_analytics(
        self, 
        start_date: str, 
        end_date: str,
        dimensions: Optional[List[str]] = None,
        row_limit: int = 100
    ) -> Dict:
        """
        検索アナリティクスデータを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            dimensions: ディメンション（query, page, country, device など）
            row_limit: 取得行数
            
        Returns:
            検索アナリティクスデータの辞書
        """
        if dimensions is None:
            dimensions = ['query']
        
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': row_limit
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()
        
        return response
    
    def get_overview(self, start_date: str, end_date: str) -> Dict:
        """
        検索パフォーマンスの概要を取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            概要データの辞書
        """
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': [],  # ディメンションなしで全体の合計を取得
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()
        
        if 'rows' not in response or len(response['rows']) == 0:
            return {
                'clicks': 0,
                'impressions': 0,
                'ctr': 0.0,
                'position': 0.0
            }
        
        row = response['rows'][0]
        
        return {
            'clicks': int(row.get('clicks', 0)),
            'impressions': int(row.get('impressions', 0)),
            'ctr': float(row.get('ctr', 0)),
            'position': float(row.get('position', 0))
        }
    
    def get_top_queries(
        self, 
        start_date: str, 
        end_date: str,
        limit: int = 20
    ) -> List[Dict]:
        """
        上位検索クエリを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            limit: 取得件数
            
        Returns:
            上位クエリのリスト
        """
        response = self.get_search_analytics(
            start_date=start_date,
            end_date=end_date,
            dimensions=['query'],
            row_limit=limit
        )
        
        queries = []
        
        if 'rows' in response:
            for row in response['rows']:
                queries.append({
                    'query': row['keys'][0],
                    'clicks': int(row.get('clicks', 0)),
                    'impressions': int(row.get('impressions', 0)),
                    'ctr': float(row.get('ctr', 0)),
                    'position': float(row.get('position', 0))
                })
        
        return queries
    
    def get_top_pages(
        self, 
        start_date: str, 
        end_date: str,
        limit: int = 20
    ) -> List[Dict]:
        """
        上位ページを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            limit: 取得件数
            
        Returns:
            上位ページのリスト
        """
        response = self.get_search_analytics(
            start_date=start_date,
            end_date=end_date,
            dimensions=['page'],
            row_limit=limit
        )
        
        pages = []
        
        if 'rows' in response:
            for row in response['rows']:
                pages.append({
                    'page': row['keys'][0],
                    'clicks': int(row.get('clicks', 0)),
                    'impressions': int(row.get('impressions', 0)),
                    'ctr': float(row.get('ctr', 0)),
                    'position': float(row.get('position', 0))
                })
        
        return pages
    
    def get_performance_by_country(
        self, 
        start_date: str, 
        end_date: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        国別パフォーマンスを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            limit: 取得件数
            
        Returns:
            国別パフォーマンスのリスト
        """
        response = self.get_search_analytics(
            start_date=start_date,
            end_date=end_date,
            dimensions=['country'],
            row_limit=limit
        )
        
        countries = []
        
        if 'rows' in response:
            for row in response['rows']:
                countries.append({
                    'country': row['keys'][0],
                    'clicks': int(row.get('clicks', 0)),
                    'impressions': int(row.get('impressions', 0)),
                    'ctr': float(row.get('ctr', 0)),
                    'position': float(row.get('position', 0))
                })
        
        return countries
    
    def get_performance_by_device(
        self, 
        start_date: str, 
        end_date: str
    ) -> List[Dict]:
        """
        デバイス別パフォーマンスを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            デバイス別パフォーマンスのリスト
        """
        response = self.get_search_analytics(
            start_date=start_date,
            end_date=end_date,
            dimensions=['device']
        )
        
        devices = []
        
        if 'rows' in response:
            for row in response['rows']:
                devices.append({
                    'device': row['keys'][0],
                    'clicks': int(row.get('clicks', 0)),
                    'impressions': int(row.get('impressions', 0)),
                    'ctr': float(row.get('ctr', 0)),
                    'position': float(row.get('position', 0))
                })
        
        return devices
    
    def get_daily_performance(
        self, 
        start_date: str, 
        end_date: str
    ) -> List[Dict]:
        """
        日別パフォーマンスを取得（時系列データ）
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            日別パフォーマンスのリスト
        """
        response = self.get_search_analytics(
            start_date=start_date,
            end_date=end_date,
            dimensions=['date'],
            row_limit=1000  # 最大1000日分
        )
        
        daily_data = []
        
        if 'rows' in response:
            for row in response['rows']:
                daily_data.append({
                    'date': row['keys'][0],
                    'clicks': int(row.get('clicks', 0)),
                    'impressions': int(row.get('impressions', 0)),
                    'ctr': float(row.get('ctr', 0)),
                    'position': float(row.get('position', 0))
                })
        
        return daily_data
    
    def get_page_performance(
        self, 
        page_url: str,
        start_date: str, 
        end_date: str
    ) -> Dict:
        """
        特定ページのパフォーマンスを取得
        
        Args:
            page_url: ページ URL
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            ページパフォーマンスの辞書
        """
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'page',
                    'operator': 'equals',
                    'expression': page_url
                }]
            }],
            'rowLimit': 100
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()
        
        queries = []
        total_clicks = 0
        total_impressions = 0
        
        if 'rows' in response:
            for row in response['rows']:
                clicks = int(row.get('clicks', 0))
                impressions = int(row.get('impressions', 0))
                
                total_clicks += clicks
                total_impressions += impressions
                
                queries.append({
                    'query': row['keys'][0],
                    'clicks': clicks,
                    'impressions': impressions,
                    'ctr': float(row.get('ctr', 0)),
                    'position': float(row.get('position', 0))
                })
        
        return {
            'page_url': page_url,
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'queries': queries
        }
    
    def get_query_performance(
        self, 
        query: str,
        start_date: str, 
        end_date: str
    ) -> Dict:
        """
        特定クエリのパフォーマンスを取得
        
        Args:
            query: 検索クエリ
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            クエリパフォーマンスの辞書
        """
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'query',
                    'operator': 'equals',
                    'expression': query
                }]
            }],
            'rowLimit': 100
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()
        
        pages = []
        total_clicks = 0
        total_impressions = 0
        
        if 'rows' in response:
            for row in response['rows']:
                clicks = int(row.get('clicks', 0))
                impressions = int(row.get('impressions', 0))
                
                total_clicks += clicks
                total_impressions += impressions
                
                pages.append({
                    'page': row['keys'][0],
                    'clicks': clicks,
                    'impressions': impressions,
                    'ctr': float(row.get('ctr', 0)),
                    'position': float(row.get('position', 0))
                })
        
        return {
            'query': query,
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'pages': pages
        }
    
    def get_sitemaps(self) -> List[Dict]:
        """
        サイトマップ一覧を取得
        
        Returns:
            サイトマップのリスト
        """
        try:
            response = self.service.sitemaps().list(
                siteUrl=self.site_url
            ).execute()
            
            sitemaps = []
            
            if 'sitemap' in response:
                for sitemap in response['sitemap']:
                    sitemaps.append({
                        'path': sitemap.get('path'),
                        'last_submitted': sitemap.get('lastSubmitted'),
                        'is_pending': sitemap.get('isPending', False),
                        'is_sitemaps_index': sitemap.get('isSitemapsIndex', False)
                    })
            
            return sitemaps
        except Exception as e:
            print(f"サイトマップ取得エラー: {e}")
            return []
    
    def get_url_inspection(self, page_url: str) -> Dict:
        """
        URL 検査情報を取得
        
        Args:
            page_url: ページ URL
            
        Returns:
            URL 検査結果の辞書
        """
        try:
            request = {
                'inspectionUrl': page_url,
                'siteUrl': self.site_url
            }
            
            response = self.service.urlInspection().index().inspect(
                body=request
            ).execute()
            
            return response
        except Exception as e:
            print(f"URL 検査エラー: {e}")
            return {}


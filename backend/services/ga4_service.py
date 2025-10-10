"""
Google Analytics 4 (GA4) データ取得サービス
"""
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    RunRealtimeReportRequest,
)
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv()


class GA4Service:
    """Google Analytics 4 データを取得するサービス"""
    
    def __init__(self, credentials: Credentials):
        """
        初期化
        
        Args:
            credentials: Google OAuth 2.0 認証情報
        """
        self.credentials = credentials
        self.client = BetaAnalyticsDataClient(credentials=credentials)
        self.property_id = os.getenv('GA4_PROPERTY_ID')
        
        if not self.property_id:
            raise ValueError("GA4_PROPERTY_ID が環境変数に設定されていません")
    
    def get_realtime_data(self) -> Dict:
        """
        リアルタイムデータを取得
        
        Returns:
            リアルタイムデータの辞書
        """
        request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[
                Dimension(name="country"),
                Dimension(name="city"),
            ],
            metrics=[
                Metric(name="activeUsers"),
            ],
        )
        
        response = self.client.run_realtime_report(request)
        
        # データを整形
        data = {
            'active_users': 0,
            'locations': []
        }
        
        for row in response.rows:
            users = int(row.metric_values[0].value)
            data['active_users'] += users
            
            if len(row.dimension_values) >= 2:
                country = row.dimension_values[0].value
                city = row.dimension_values[1].value
                data['locations'].append({
                    'country': country,
                    'city': city,
                    'users': users
                })
        
        return data
    
    def get_traffic_overview(self, start_date: str, end_date: str) -> Dict:
        """
        トラフィック概要を取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            トラフィック概要の辞書
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="newUsers"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
        )
        
        response = self.client.run_report(request)
        
        if not response.rows:
            return {}
        
        row = response.rows[0]
        
        return {
            'sessions': int(row.metric_values[0].value),
            'total_users': int(row.metric_values[1].value),
            'new_users': int(row.metric_values[2].value),
            'page_views': int(row.metric_values[3].value),
            'avg_session_duration': float(row.metric_values[4].value),
            'bounce_rate': float(row.metric_values[5].value),
        }
    
    def get_traffic_by_source(self, start_date: str, end_date: str, limit: int = 10) -> List[Dict]:
        """
        トラフィックソース別のデータを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            limit: 取得件数
            
        Returns:
            トラフィックソースのリスト
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[
                Dimension(name="sessionSource"),
                Dimension(name="sessionMedium"),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
            ],
            limit=limit,
        )
        
        response = self.client.run_report(request)
        
        sources = []
        for row in response.rows:
            sources.append({
                'source': row.dimension_values[0].value,
                'medium': row.dimension_values[1].value,
                'sessions': int(row.metric_values[0].value),
                'users': int(row.metric_values[1].value),
                'page_views': int(row.metric_values[2].value),
            })
        
        return sources
    
    def get_top_pages(self, start_date: str, end_date: str, limit: int = 20) -> List[Dict]:
        """
        人気ページランキングを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            limit: 取得件数
            
        Returns:
            人気ページのリスト
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[
                Dimension(name="pagePath"),
                Dimension(name="pageTitle"),
            ],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="totalUsers"),
                Metric(name="averageSessionDuration"),
            ],
            limit=limit,
        )
        
        response = self.client.run_report(request)
        
        pages = []
        for row in response.rows:
            pages.append({
                'path': row.dimension_values[0].value,
                'title': row.dimension_values[1].value,
                'page_views': int(row.metric_values[0].value),
                'users': int(row.metric_values[1].value),
                'avg_time': float(row.metric_values[2].value),
            })
        
        return pages
    
    def get_traffic_by_country(self, start_date: str, end_date: str, limit: int = 10) -> List[Dict]:
        """
        国別トラフィックを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            limit: 取得件数
            
        Returns:
            国別トラフィックのリスト
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[
                Dimension(name="country"),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
            ],
            limit=limit,
        )
        
        response = self.client.run_report(request)
        
        countries = []
        for row in response.rows:
            countries.append({
                'country': row.dimension_values[0].value,
                'sessions': int(row.metric_values[0].value),
                'users': int(row.metric_values[1].value),
                'page_views': int(row.metric_values[2].value),
            })
        
        return countries
    
    def get_traffic_by_device(self, start_date: str, end_date: str) -> List[Dict]:
        """
        デバイス別トラフィックを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            デバイス別トラフィックのリスト
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[
                Dimension(name="deviceCategory"),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="bounceRate"),
            ],
        )
        
        response = self.client.run_report(request)
        
        devices = []
        for row in response.rows:
            devices.append({
                'device': row.dimension_values[0].value,
                'sessions': int(row.metric_values[0].value),
                'users': int(row.metric_values[1].value),
                'bounce_rate': float(row.metric_values[2].value),
            })
        
        return devices
    
    def get_daily_traffic(self, start_date: str, end_date: str) -> List[Dict]:
        """
        日別トラフィックを取得（時系列データ）
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            日別トラフィックのリスト
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[
                Dimension(name="date"),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
            ],
        )
        
        response = self.client.run_report(request)
        
        daily_data = []
        for row in response.rows:
            date_str = row.dimension_values[0].value
            # YYYYMMDD -> YYYY-MM-DD に変換
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            
            daily_data.append({
                'date': formatted_date,
                'sessions': int(row.metric_values[0].value),
                'users': int(row.metric_values[1].value),
                'page_views': int(row.metric_values[2].value),
            })
        
        return daily_data
    
    def get_organic_search_traffic(self, start_date: str, end_date: str) -> Dict:
        """
        オーガニック検索トラフィックを取得
        
        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            
        Returns:
            オーガニック検索トラフィックの辞書
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[
                Dimension(name="sessionSource"),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
            ],
            dimension_filter={
                "filter": {
                    "field_name": "sessionMedium",
                    "string_filter": {
                        "match_type": "EXACT",
                        "value": "organic"
                    }
                }
            }
        )
        
        response = self.client.run_report(request)
        
        organic_data = {
            'total_sessions': 0,
            'total_users': 0,
            'total_page_views': 0,
            'by_source': []
        }
        
        for row in response.rows:
            sessions = int(row.metric_values[0].value)
            users = int(row.metric_values[1].value)
            page_views = int(row.metric_values[2].value)
            
            organic_data['total_sessions'] += sessions
            organic_data['total_users'] += users
            organic_data['total_page_views'] += page_views
            
            organic_data['by_source'].append({
                'source': row.dimension_values[0].value,
                'sessions': sessions,
                'users': users,
                'page_views': page_views,
            })
        
        return organic_data


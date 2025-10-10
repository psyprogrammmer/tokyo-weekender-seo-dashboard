"""
Google OAuth 2.0 認証サービス
GA4 と GSC への接続に使用
"""
import os
import json
from typing import Optional, Dict
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

# OAuth スコープの定義
SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',  # GA4
    'https://www.googleapis.com/auth/webmasters.readonly',  # GSC
]

# 認証情報の保存パス
TOKEN_PATH = Path('data/credentials/google_token.json')
CLIENT_SECRET_PATH = Path('data/credentials/google_client_secret.json')


class GoogleAuthService:
    """Google OAuth 2.0 認証を管理するサービス"""
    
    def __init__(self):
        """初期化"""
        self.credentials: Optional[Credentials] = None
        self.token_path = TOKEN_PATH
        self.client_secret_path = CLIENT_SECRET_PATH
        
        # 認証情報ディレクトリの作成
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_authorization_url(self, redirect_uri: str) -> str:
        """
        OAuth 2.0 認証 URL を取得
        
        Args:
            redirect_uri: リダイレクト URI
            
        Returns:
            認証 URL
        """
        if not self.client_secret_path.exists():
            raise FileNotFoundError(
                f"クライアントシークレットファイルが見つかりません: {self.client_secret_path}\n"
                "Google Cloud Console で OAuth 2.0 クライアント ID を作成し、"
                "JSON ファイルをダウンロードしてください。"
            )
        
        flow = Flow.from_client_secrets_file(
            str(self.client_secret_path),
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return auth_url
    
    def handle_authorization_callback(self, authorization_response: str, redirect_uri: str) -> Dict:
        """
        OAuth 2.0 コールバックを処理してトークンを取得
        
        Args:
            authorization_response: 認証レスポンス URL
            redirect_uri: リダイレクト URI
            
        Returns:
            認証情報の辞書
        """
        flow = Flow.from_client_secrets_file(
            str(self.client_secret_path),
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        # 認証コードを使用してトークンを取得
        flow.fetch_token(authorization_response=authorization_response)
        
        # クレデンシャルを保存
        self.credentials = flow.credentials
        self._save_credentials()
        
        return {
            'success': True,
            'message': 'Google アカウントとの接続に成功しました',
            'scopes': self.credentials.scopes
        }
    
    def get_credentials(self) -> Optional[Credentials]:
        """
        保存された認証情報を取得
        
        Returns:
            Credentials オブジェクト、または None
        """
        if self.credentials and self.credentials.valid:
            return self.credentials
        
        # トークンファイルから読み込み
        if self.token_path.exists():
            self.credentials = Credentials.from_authorized_user_file(
                str(self.token_path),
                SCOPES
            )
        
        # トークンが期限切れの場合はリフレッシュ
        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            try:
                self.credentials.refresh(Request())
                self._save_credentials()
            except Exception as e:
                print(f"トークンのリフレッシュに失敗: {e}")
                return None
        
        return self.credentials if self.credentials and self.credentials.valid else None
    
    def _save_credentials(self):
        """認証情報をファイルに保存"""
        if self.credentials:
            with open(self.token_path, 'w') as token_file:
                token_file.write(self.credentials.to_json())
    
    def revoke_credentials(self) -> Dict:
        """
        認証情報を取り消し（削除）
        
        Returns:
            結果の辞書
        """
        if self.token_path.exists():
            self.token_path.unlink()
        
        self.credentials = None
        
        return {
            'success': True,
            'message': 'Google アカウントとの接続が解除されました'
        }
    
    def is_authenticated(self) -> bool:
        """
        認証済みかどうかを確認
        
        Returns:
            認証済みの場合 True
        """
        creds = self.get_credentials()
        return creds is not None and creds.valid
    
    def get_auth_status(self) -> Dict:
        """
        認証ステータスを取得
        
        Returns:
            ステータスの辞書
        """
        is_auth = self.is_authenticated()
        
        status = {
            'authenticated': is_auth,
            'has_ga4_access': is_auth,
            'has_gsc_access': is_auth,
        }
        
        if is_auth and self.credentials:
            status['scopes'] = self.credentials.scopes
        
        return status


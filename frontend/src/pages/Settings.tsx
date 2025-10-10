import React, { useState, useEffect } from 'react'
import { Settings as SettingsIcon, Upload, Database, RefreshCw, CheckCircle, XCircle, ExternalLink } from 'lucide-react'
import { api } from '../utils/api'

interface GoogleAuthStatus {
  authenticated: boolean
  has_ga4_access?: boolean
  has_gsc_access?: boolean
  scopes?: string[]
  error?: string
}

const Settings: React.FC = () => {
  const [googleAuthStatus, setGoogleAuthStatus] = useState<GoogleAuthStatus | null>(null)
  const [isConnecting, setIsConnecting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Google 認証ステータスを確認
  const checkGoogleAuthStatus = async () => {
    try {
      const response = await api.get('/google/auth-status')
      setGoogleAuthStatus(response.data)
    } catch (err) {
      console.error('Failed to check Google auth status:', err)
      setGoogleAuthStatus({ authenticated: false })
    }
  }

  // 初回ロード時にステータスを確認
  useEffect(() => {
    checkGoogleAuthStatus()
    
    // URL パラメータから認証コードを取得
    const urlParams = new URLSearchParams(window.location.search)
    const code = urlParams.get('code')
    const state = urlParams.get('state')
    
    if (code) {
      // 認証コードを Backend に送信
      handleAuthCallback(code, state)
    }
    
    // ポップアップからのメッセージを受信
    const handleMessage = (event: MessageEvent) => {
      // セキュリティ: 同じオリジンからのメッセージのみ受け入れ
      if (event.origin !== window.location.origin) return
      
      if (event.data.type === 'google-auth-success') {
        // 認証成功
        setIsConnecting(false)
        checkGoogleAuthStatus()
        alert('Google アカウントとの接続に成功しました！')
      } else if (event.data.type === 'google-auth-error') {
        // 認証失敗
        setIsConnecting(false)
        setError(event.data.error || '認証に失敗しました')
      }
    }
    
    window.addEventListener('message', handleMessage)
    
    return () => {
      window.removeEventListener('message', handleMessage)
    }
  }, [])
  
  // OAuth コールバックを処理
  const handleAuthCallback = async (code: string, state: string | null) => {
    try {
      setIsConnecting(true)
      
      // 認証コードを含む完全な URL を構築
      const callbackUrl = `${window.location.origin}${window.location.pathname}?code=${code}${state ? `&state=${state}` : ''}`
      
      // Backend に送信
      const response = await api.post('/google/auth-callback', null, {
        params: { authorization_response: callbackUrl }
      })
      
      if (response.data.success) {
        // URL から認証パラメータを削除
        window.history.replaceState({}, document.title, window.location.pathname)
        
        // 認証ステータスを再確認
        await checkGoogleAuthStatus()
        
        // ポップアップ内で実行されている場合は閉じる
        if (window.opener && !window.opener.closed) {
          // 親ウィンドウに認証完了を通知
          window.opener.postMessage({ type: 'google-auth-success' }, window.location.origin)
          window.close()
        } else {
          // 通常のウィンドウの場合はアラート表示
          alert('Google アカウントとの接続に成功しました！')
        }
      }
    } catch (err: any) {
      console.error('Failed to handle auth callback:', err)
      setError(err.response?.data?.detail || '認証の処理に失敗しました')
      
      // URL から認証パラメータを削除
      window.history.replaceState({}, document.title, window.location.pathname)
      
      // ポップアップ内で実行されている場合は閉じる
      if (window.opener && !window.opener.closed) {
        window.opener.postMessage({ type: 'google-auth-error', error: err.message }, window.location.origin)
        window.close()
      }
    } finally {
      setIsConnecting(false)
    }
  }

  // Google アカウントに接続
  const handleConnectGoogle = async () => {
    try {
      setIsConnecting(true)
      setError(null)
      
      // 認証 URL を取得
      const response = await api.get('/google/auth-url')
      const authUrl = response.data.auth_url
      
      // 新しいウィンドウで認証ページを開く
      const width = 600
      const height = 700
      const left = window.screen.width / 2 - width / 2
      const top = window.screen.height / 2 - height / 2
      
      const authWindow = window.open(
        authUrl,
        'Google Auth',
        `width=${width},height=${height},top=${top},left=${left}`
      )
      
      // ポップアップがブロックされたかチェック
      if (!authWindow) {
        setError('ポップアップがブロックされました。ブラウザの設定を確認してください。')
        setIsConnecting(false)
        return
      }
      
      // ウィンドウが閉じられたら認証ステータスを再確認
      const checkWindowClosed = setInterval(() => {
        if (authWindow.closed) {
          clearInterval(checkWindowClosed)
          setIsConnecting(false)
          checkGoogleAuthStatus()
        }
      }, 500)
      
    } catch (err: any) {
      console.error('Failed to connect Google account:', err)
      setError(err.response?.data?.detail || '接続に失敗しました')
      setIsConnecting(false)
    }
  }

  // Google アカウント接続を解除
  const handleDisconnectGoogle = async () => {
    if (!confirm('Google アカウントとの接続を解除しますか？')) {
      return
    }
    
    try {
      await api.post('/google/revoke')
      setGoogleAuthStatus({ authenticated: false })
      alert('Google アカウントとの接続を解除しました')
    } catch (err: any) {
      console.error('Failed to disconnect Google account:', err)
      setError(err.response?.data?.detail || '接続解除に失敗しました')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-gray-600">
          Data management and system configuration
        </p>
      </div>

      {/* Google API 接続 */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Google API 接続
        </h3>
        
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}
        
        <div className="space-y-4">
          {googleAuthStatus && (
            <div className="p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center space-x-2">
                    {googleAuthStatus.authenticated ? (
                      <>
                        <CheckCircle className="h-5 w-5 text-green-500" />
                        <h4 className="font-medium text-gray-900">接続済み</h4>
                      </>
                    ) : (
                      <>
                        <XCircle className="h-5 w-5 text-gray-400" />
                        <h4 className="font-medium text-gray-900">未接続</h4>
                      </>
                    )}
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    {googleAuthStatus.authenticated
                      ? 'Google Analytics 4 と Search Console のデータにアクセスできます'
                      : 'Google アカウントに接続してリアルタイムデータを取得'}
                  </p>
                  {googleAuthStatus.authenticated && (
                    <div className="mt-2 space-y-1">
                      {googleAuthStatus.has_ga4_access && (
                        <div className="flex items-center text-sm text-green-600">
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Google Analytics 4
                        </div>
                      )}
                      {googleAuthStatus.has_gsc_access && (
                        <div className="flex items-center text-sm text-green-600">
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Google Search Console
                        </div>
                      )}
                    </div>
                  )}
                </div>
                <div>
                  {googleAuthStatus.authenticated ? (
                    <button
                      onClick={handleDisconnectGoogle}
                      className="btn-secondary text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      接続解除
                    </button>
                  ) : (
                    <button
                      onClick={handleConnectGoogle}
                      disabled={isConnecting}
                      className="btn-primary flex items-center space-x-2"
                    >
                      {isConnecting ? (
                        <>
                          <RefreshCw className="h-4 w-4 animate-spin" />
                          <span>接続中...</span>
                        </>
                      ) : (
                        <>
                          <ExternalLink className="h-4 w-4" />
                          <span>Google アカウントに接続</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}
          
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">接続手順</h4>
            <ol className="text-sm text-blue-700 space-y-1 list-decimal list-inside">
              <li>上記の「Google アカウントに接続」ボタンをクリック</li>
              <li>Google アカウントでログイン</li>
              <li>Google Analytics と Search Console へのアクセスを許可</li>
              <li>接続完了後、ダッシュボードでリアルタイムデータを確認</li>
            </ol>
          </div>
        </div>
      </div>

      {/* データ管理 */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Database className="h-5 w-5 mr-2" />
          Data Management
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">Tokyo Weekender Keyword Data</h4>
              <p className="text-sm text-gray-500">Current data: 60,872 keywords</p>
            </div>
            <button className="btn-secondary flex items-center space-x-2">
              <Upload className="h-4 w-4" />
              <span>Update</span>
            </button>
          </div>
          
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">Competitor Site Data</h4>
              <p className="text-sm text-gray-500">Uploaded data: 0 items</p>
            </div>
            <button className="btn-secondary flex items-center space-x-2">
              <Upload className="h-4 w-4" />
              <span>Upload</span>
            </button>
          </div>
          
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">Google Search Console Data</h4>
              <p className="text-sm text-gray-500">
                {googleAuthStatus?.authenticated ? '接続済み（上記の Google API 接続を参照）' : '未接続（上記の Google API 接続を参照）'}
              </p>
            </div>
            {googleAuthStatus?.authenticated && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                <CheckCircle className="h-4 w-4 mr-1" />
                Connected
              </span>
            )}
          </div>
        </div>
      </div>

      {/* 分析設定 */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <SettingsIcon className="h-5 w-5 mr-2" />
          Analysis Settings
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              High Performance Keywords Definition
            </label>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Minimum Search Volume</label>
                <input
                  type="number"
                  defaultValue="100"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">Maximum Position</label>
                <input
                  type="number"
                  defaultValue="10"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Improvement Opportunity Keywords Definition
            </label>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Minimum Search Volume</label>
                <input
                  type="number"
                  defaultValue="50"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">Position Range</label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
                  <option value="11-20">11-20</option>
                  <option value="11-30">11-30</option>
                  <option value="11-50">11-50</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* システム操作 */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <RefreshCw className="h-5 w-5 mr-2" />
          System Operations
        </h3>
        <div className="space-y-3">
          <button className="btn-primary w-full sm:w-auto">
            Recalculate Analysis Data
          </button>
          <button className="btn-secondary w-full sm:w-auto">
            Clear Cache
          </button>
          <button className="btn-secondary w-full sm:w-auto text-red-600 hover:text-red-700 hover:bg-red-50">
            Reset All Data
          </button>
        </div>
      </div>
    </div>
  )
}

export default Settings

import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Alert, AlertDescription } from './ui/alert'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'

const GoogleCallback = () => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { updateUser } = useAuth()
  const [status, setStatus] = useState('processing') // processing, success, error
  const [message, setMessage] = useState('Processing Google authentication...')

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const token = searchParams.get('token')
        const userParam = searchParams.get('user')
        const error = searchParams.get('error')

        if (error) {
          setStatus('error')
          setMessage('Google authentication failed. Please try again.')
          setTimeout(() => navigate('/login'), 3000)
          return
        }

        if (token && userParam) {
          // Decode user data
          const userData = JSON.parse(decodeURIComponent(userParam))
          
          // Store token and user data
          localStorage.setItem('token', token)
          localStorage.setItem('user', JSON.stringify(userData))
          
          // Update auth context
          updateUser(userData)
          
          setStatus('success')
          setMessage('Successfully authenticated with Google!')
          
          // Redirect to intended destination or dashboard
          const redirectTo = localStorage.getItem('loginRedirect') || '/dashboard'
          localStorage.removeItem('loginRedirect')
          
          setTimeout(() => {
            navigate(redirectTo, { replace: true })
          }, 2000)
        } else {
          setStatus('error')
          setMessage('Invalid authentication response. Please try again.')
          setTimeout(() => navigate('/login'), 3000)
        }
      } catch (error) {
        console.error('Google callback error:', error)
        setStatus('error')
        setMessage('An error occurred during authentication. Please try again.')
        setTimeout(() => navigate('/login'), 3000)
      }
    }

    handleCallback()
  }, [searchParams, navigate, updateUser])

  const getIcon = () => {
    switch (status) {
      case 'processing':
        return <Loader2 className="h-8 w-8 animate-spin text-primary" />
      case 'success':
        return <CheckCircle className="h-8 w-8 text-green-500" />
      case 'error':
        return <XCircle className="h-8 w-8 text-red-500" />
      default:
        return <Loader2 className="h-8 w-8 animate-spin text-primary" />
    }
  }

  const getAlertVariant = () => {
    switch (status) {
      case 'success':
        return 'default'
      case 'error':
        return 'destructive'
      default:
        return 'default'
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/5 to-accent/5 px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            {getIcon()}
          </div>
          <CardTitle className="text-xl">
            {status === 'processing' && 'Authenticating...'}
            {status === 'success' && 'Authentication Successful!'}
            {status === 'error' && 'Authentication Failed'}
          </CardTitle>
          <CardDescription>
            {status === 'processing' && 'Please wait while we complete your Google authentication.'}
            {status === 'success' && 'You will be redirected shortly.'}
            {status === 'error' && 'You will be redirected to the login page.'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Alert variant={getAlertVariant()}>
            <AlertDescription className="text-center">
              {message}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    </div>
  )
}

export default GoogleCallback


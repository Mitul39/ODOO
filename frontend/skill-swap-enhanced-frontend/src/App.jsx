import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './hooks/useAuth'
import ProtectedRoute from './components/ProtectedRoute'
import Header from './components/Header'
import Homepage from './components/Homepage'
import Login from './components/Login'
import Register from './components/Register'
import GoogleCallback from './components/GoogleCallback'
import CreateProfile from './components/CreateProfile'
import BrowseUsers from './components/BrowseUsers'
import Dashboard from './components/Dashboard'
import Profile from './components/Profile'
import Sessions from './components/Sessions'
import Calendar from './components/Calendar'
import Leaderboard from './components/Leaderboard'
import Notifications from './components/Notifications'
import SkillSuggestions from './components/SkillSuggestions'
import AboutUs from './components/AboutUs'
import WhySkillSwap from './components/WhySkillSwap'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-background">
          <Header />
          <main>
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<Homepage />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/about" element={<AboutUs />} />
              <Route path="/why-skillswap" element={<WhySkillSwap />} />
              <Route path="/auth/google/callback" element={<GoogleCallback />} />
              
              {/* Protected routes */}
              <Route path="/create-profile" element={
                <ProtectedRoute>
                  <CreateProfile />
                </ProtectedRoute>
              } />
              <Route path="/browse" element={
                <ProtectedRoute>
                  <BrowseUsers />
                </ProtectedRoute>
              } />
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="/profile/:userId?" element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              } />
              <Route path="/sessions" element={
                <ProtectedRoute>
                  <Sessions />
                </ProtectedRoute>
              } />
              <Route path="/calendar" element={
                <ProtectedRoute>
                  <Calendar />
                </ProtectedRoute>
              } />
              <Route path="/leaderboard" element={
                <ProtectedRoute>
                  <Leaderboard />
                </ProtectedRoute>
              } />
              <Route path="/notifications" element={
                <ProtectedRoute>
                  <Notifications />
                </ProtectedRoute>
              } />
              <Route path="/skill-suggestions" element={
                <ProtectedRoute>
                  <SkillSuggestions />
                </ProtectedRoute>
              } />
              
              {/* Catch all route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App


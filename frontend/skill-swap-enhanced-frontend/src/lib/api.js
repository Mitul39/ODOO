import axios from 'axios'

// API Configuration
const API_BASE_URL = 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          
          const { token } = response.data
          localStorage.setItem('token', token)
          
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('user')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  googleLogin: () => window.location.href = `${API_BASE_URL}/auth/google`,
  verify: () => api.get('/auth/verify'),
  logout: () => api.post('/auth/logout'),
  refresh: () => api.post('/auth/refresh'),
}

// User API
export const userAPI = {
  getUsers: (params = {}) => api.get('/api/users', { params }),
  getUser: (userId) => api.get(`/api/users/${userId}`),
  updateProfile: (userData) => api.post('/api/users', userData),
  updateUser: (userId, userData) => api.put(`/api/users/${userId}`, userData),
  uploadImage: (formData) => api.post('/api/users/upload-image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getUserStats: (userId) => api.get(`/api/users/${userId}/stats`),
  deleteUser: (userId) => api.delete(`/api/users/${userId}`),
}

// Swap Request API
export const swapRequestAPI = {
  createRequest: (requestData) => api.post('/api/swap-requests', requestData),
  getSentRequests: (userId) => api.get(`/api/swap-requests/sent/${userId}`),
  getReceivedRequests: (userId) => api.get(`/api/swap-requests/received/${userId}`),
  acceptRequest: (requestId) => api.put(`/api/swap-requests/${requestId}/accept`),
  rejectRequest: (requestId) => api.put(`/api/swap-requests/${requestId}/reject`),
  deleteRequest: (requestId) => api.delete(`/api/swap-requests/${requestId}`),
}

// Session API
export const sessionAPI = {
  createSession: (sessionData) => api.post('/api/sessions', sessionData),
  getUserSessions: (userId) => api.get(`/api/sessions/user/${userId}`),
  updateSession: (sessionId, sessionData) => api.put(`/api/sessions/${sessionId}`, sessionData),
  deleteSession: (sessionId) => api.delete(`/api/sessions/${sessionId}`),
  getUpcomingSessions: () => api.get('/api/sessions/upcoming'),
}

// Badge API
export const badgeAPI = {
  getLeaderboard: () => api.get('/api/badges/leaderboard'),
  getBadgeStats: () => api.get('/api/badges/stats'),
  getUserBadges: (userId) => api.get(`/api/badges/user/${userId}`),
  updateUserBadge: (userId) => api.post(`/api/badges/update/${userId}`),
}

// Notification API
export const notificationAPI = {
  getUserNotifications: (userId) => api.get(`/api/notifications/user/${userId}`),
  markNotificationRead: (notificationId) => api.put(`/api/notifications/${notificationId}/read`),
  markAllNotificationsRead: () => api.put('/api/notifications/mark-all-read'),
  sendNotification: (notificationData) => api.post('/api/notifications/send', notificationData),
  updateNotificationPreferences: (userId, preferences) => api.put(`/api/notifications/preferences/${userId}`, preferences),
}

// Skill Suggestion API
export const skillSuggestionAPI = {
  getSkillSuggestions: (userId) => api.get(`/api/skill-suggestions/${userId}`),
  getSkillCategories: () => api.get('/api/skill-categories'),
  searchSkills: (query) => api.get('/api/skills/search', { params: { q: query } }),
  getPopularSkills: () => api.get('/api/skills/popular'),
}

export default api


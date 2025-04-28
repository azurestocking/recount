import axios from 'axios';

// Create an axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API calls
export const authAPI = {
  login: (userAccount, userPassword) => api.post('/auth/login', { user_account: userAccount, user_password: userPassword }),
  register: (userData) => api.post('/auth/register', userData),
};

// Chat API calls
export const chatAPI = {
  sendMessage: (messageData) => api.post('/chat/chat', messageData),
  getConversationHistory: (conversationId) => 
    api.get(`/chat/conversations/${conversationId}/history`),
  getTimeline: (conversationId) => 
    api.get(`/chat/conversations/${conversationId}/timeline`),
  getUserConversations: (userId) => 
    api.get(`/chat/users/${userId}/conversations`),
};

export default api; 
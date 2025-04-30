import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Create an axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
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

// Helper to get auth headers for fetch
function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

// Incident API
export async function getIncidents() {
  const res = await fetch(`${API_URL}/incidents`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error('Failed to fetch incidents');
  return res.json();
}

export async function getIncident(id) {
  const res = await fetch(`${API_URL}/incidents/${id}`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error('Failed to fetch incident');
  return res.json();
}

export async function createIncident(data) {
  const res = await fetch(`${API_URL}/incidents`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create incident');
  return res.json();
}

export async function updateIncident(id, data) {
  const res = await fetch(`${API_URL}/incidents/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to update incident');
  return res.json();
}

export async function getTimeline(incidentId) {
  const res = await fetch(`${API_URL}/incidents/${incidentId}/timeline`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error('Failed to fetch timeline');
  return res.json();
}

export async function addTimelineEvent(incidentId, data) {
  const res = await fetch(`${API_URL}/incidents/${incidentId}/timeline`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to add timeline event');
  return res.json();
}

export async function getExhibits(incidentId) {
  const res = await fetch(`${API_URL}/incidents/${incidentId}/evidence`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error('Failed to fetch exhibits');
  return res.json();
}

export async function deleteIncident(id) {
  const res = await fetch(`${API_URL}/incidents/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error('Failed to delete incident');
  return true;
}

export const getIncidentConversations = async (incidentId) => {
  const response = await fetch(`${API_URL}/incidents/${incidentId}/conversations`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
  if (!response.ok) {
    throw new Error('Failed to fetch conversations');
  }
  return response.json();
};

export default api; 
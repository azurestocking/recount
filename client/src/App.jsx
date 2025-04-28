import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import Login from './components/auth/Login';
import Timeline from './components/timeline/Timeline';
import ResourceList from './components/resources/ResourceList';
import Signup from './components/auth/Signup';
import { AuthProvider, useAuth } from './context/AuthContext';
import DialogueText from './pages/DialogueText';
import DialogueVoice from './pages/DialogueVoice';

// Protected Route component
const ProtectedRoute = ({ children, allowGuest = true }) => {
  const { isAuthenticated, loading, isGuest } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  // If the route doesn't allow guests and the user is a guest, redirect to login
  if (!allowGuest && isGuest()) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected routes with MainLayout */}
        <Route path="/dashboard" element={
          <ProtectedRoute allowGuest={true}>
            <MainLayout>
              <Dashboard />
            </MainLayout>
          </ProtectedRoute>
        } />
        {/* <Route path="/timeline" element={
          <ProtectedRoute allowGuest={true}>
            <MainLayout>
              <Timeline />
            </MainLayout>
          </ProtectedRoute>
        } /> */}
        <Route path="/resources" element={
          <ProtectedRoute allowGuest={true}>
            <MainLayout>
              <ResourceList />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/dialogue/text" element={
          <ProtectedRoute allowGuest={true}>
            <MainLayout>
              <DialogueText />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/dialogue/voice" element={
          <ProtectedRoute allowGuest={true}>
            <MainLayout>
              <DialogueVoice />
            </MainLayout>
          </ProtectedRoute>
        } />
         {/* <Route path="/archive" element={
          <ProtectedRoute allowGuest={true}>
            <MainLayout>
              <Archive />
            </MainLayout>
          </ProtectedRoute>
        } /> */}
      </Routes>
    </AuthProvider>
  );
}

export default App; 
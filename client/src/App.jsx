import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import Login from './components/auth/Login';
import Timeline from './components/timeline/Timeline';
import ResourceList from './components/resources/ResourceList';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />

        {/* Protected routes with MainLayout */}
        <Route path="/dashboard" element={
          <MainLayout>
            <Dashboard />
          </MainLayout>
        } />
        <Route path="/timeline" element={
          <MainLayout>
            <Timeline />
          </MainLayout>
        } />
        <Route path="/resources" element={
          <MainLayout>
            <ResourceList />
          </MainLayout>
        } />
      </Routes>
    </Router>
  );
}

export default App; 
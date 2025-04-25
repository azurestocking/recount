import React from 'react';
import ActionGrid from '../components/dashboard/ActionGrid';
import ChatInterface from '../components/chat/ChatInterface';

const Dashboard = () => {
  return (
    <div className="container mx-auto p-4">
      <div className="flex flex-col items-center mb-8">
        {/* Logo */}
        <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mb-4">
          <span className="text-white text-2xl font-bold">R</span>
        </div>
        <h1 className="text-2xl font-bold mb-2">Recount</h1>
      </div>

      {/* Main Actions */}
      <ActionGrid />

      {/* Chat Interface */}
      <div className="mt-8">
        <ChatInterface />
      </div>
    </div>
  );
};

export default Dashboard; 
import React from 'react';
import ActionGrid from '../components/dashboard/ActionGrid';
import ChatInterface from '../components/chat/ChatInterface';

const Dashboard = () => {
  return (
    <div className="container mx-auto p-0 my-8">
      <div className="flex flex-col items-center mb-8">
        <div className="flex flex-col items-center gap-4">
          <h1 className="leading-tight text-lg font-semibold mb-2">No worries, Jane</h1>
          <p className="text-gray-500 text-base font-normal text-center">We are here to help you understand your rights and navigate through the stressful situation.</p>
        </div>
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
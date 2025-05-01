import React from 'react';
import ActionGrid from '../components/dashboard/ActionGrid';

const Dashboard = () => {
  return (
    <div className="flex flex-col min-h-screen items-center justify-center px-4 py-20">
      <div id="hero" className="flex flex-col items-center justify-center gap-6 w-full flex-1">
        {/* Welcome Text */}
        <div className="flex flex-col items-center justify-center gap-4 w-full">
          <h1 className="text-2xl font-bold text-[#111928] text-center font-leading-tight-text-2xl-font-bold">
            No worries, Jane
          </h1>
          <p className="text-base text-gray-500 text-center font-text-base-font-normal">
            We are here to help you understand your rights and navigate through the stressful situation.
          </p>
        </div>
      </div>

      <div id="main container" className="flex flex-col items-center justify-center gap-6 w-full">
        {/* Main Actions */}
        <ActionGrid />
      </div>
    </div>
  );
};

export default Dashboard; 
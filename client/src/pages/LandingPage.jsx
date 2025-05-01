import React, { useState } from 'react';
import Login from '../components/auth/Login';
import Signup from '../components/auth/Signup';

const LandingPage = () => {
  const [showSignup, setShowSignup] = useState(false);

  const handleSignupClick = () => {
    setShowSignup(true);
  };

  const handleLoginClick = () => {
    setShowSignup(false);
  };

  return (
    <div className="flex flex-col min-h-screen items-center justify-center py-8 max-w-lg mx-auto">
      <div className="flex flex-col items-center justify-center gap-6 p-8 w-full flex-1">
        {/* Logo */}
        <div className="w-36 h-36 rounded-full flex items-center justify-center">
          <img src="/images/logo.svg" alt="logo" className="w-full h-full object-cover" />
        </div>

        {/* Welcome Text */}
        <div className="flex flex-col items-center justify-center gap-4 w-full">
          <h1 className="text-2xl font-bold text-center font-leading-tight">
            Recount
          </h1>
          <p className="text-base text-gray-500 text-center font-normal">
            Your guide through the justice process—built for survivors, powered by AI.
          </p>
        </div>
      </div>

      <div id="login-container" className="px-4 w-full">
        {showSignup ? (
          <Signup onLoginClick={handleLoginClick} />
        ) : (
          <Login onSignupClick={handleSignupClick} />
        )}
      </div>

    </div>
  );
};

export default LandingPage; 
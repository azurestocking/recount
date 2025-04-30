import React, { useState } from 'react';
import { Button, Card } from 'flowbite-react';
import { Link } from 'react-router-dom';
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
    <div className="flex flex-col min-h-screen items-center justify-center bg-white py-8">
      <div className="flex flex-col items-center justify-center gap-6 p-8 w-full flex-1">
        {/* Logo */}
        <div className="w-36 h-36 rounded-full flex items-center justify-center">
          <img src="/images/logo.svg" alt="logo" className="w-full h-full object-cover" />
        </div>

        {/* Welcome Text */}
        <div className="flex flex-col items-center justify-center gap-4 w-full">
          <h1 className="text-2xl font-bold text-[#111928] text-center font-leading-tight-text-2xl-font-bold">
            Recount
          </h1>
          <p className="text-base text-gray-500 text-center font-text-base-font-normal">
            Your guide through the justice process—built for survivors, powered by AI.
          </p>
        </div>
      </div>

      <card id="login-container" className="max-w-sm w-full border-0 shadow-none">
        {showSignup ? (
          <Signup onLoginClick={handleLoginClick} />
        ) : (
          <Login onSignupClick={handleSignupClick} />
        )}
      </card>

    </div>
  );
};

export default LandingPage; 
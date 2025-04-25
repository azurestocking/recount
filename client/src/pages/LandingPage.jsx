import React from 'react';
import { Button } from 'flowbite-react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      {/* Logo */}
      <div className="w-32 h-32 bg-blue-600 rounded-full flex items-center justify-center mb-6">
        <svg className="w-20 h-20 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
        </svg>
      </div>

      {/* Welcome Text */}
      <h1 className="text-2xl font-bold text-center mb-2">
        Welcome to Recount
      </h1>
      <p className="text-gray-600 text-center mb-8">
        Your Personal Guide for Every Step in the Legal Journey
      </p>

      {/* Buttons */}
      <div className="w-full max-w-xs space-y-4">
        <Button as={Link} to="/signup" className="w-full">
          Create an Account
        </Button>
        <Button as={Link} to="/login" color="light" className="w-full">
          Log In
        </Button>
        <Button as={Link} to="/dashboard" color="light" className="w-full">
          Continue as guest
        </Button>
      </div>

      {/* Divider */}
      <div className="flex items-center w-full max-w-xs my-6">
        <div className="flex-1 border-t border-gray-300"></div>
        <span className="px-4 text-sm text-gray-500">or</span>
        <div className="flex-1 border-t border-gray-300"></div>
      </div>

      {/* Social Login */}
      <div className="flex gap-4">
        <Button color="light" className="rounded-full w-12 h-12 p-0">
          <img src="/apple-icon.svg" alt="Apple" className="w-6 h-6" />
        </Button>
        <Button color="light" className="rounded-full w-12 h-12 p-0">
          <img src="/facebook-icon.svg" alt="Facebook" className="w-6 h-6" />
        </Button>
        <Button color="light" className="rounded-full w-12 h-12 p-0">
          <img src="/google-icon.svg" alt="Google" className="w-6 h-6" />
        </Button>
      </div>
    </div>
  );
};

export default LandingPage; 
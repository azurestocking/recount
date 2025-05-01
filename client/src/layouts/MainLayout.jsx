import React from 'react';
import { Navbar, Button, Avatar, Dropdown, Badge } from 'flowbite-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const MainLayout = ({ children }) => {
  const { user, logout, isGuest } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-gray-50 max-w-lg mx-auto">
      {/* header */}
      <div className="fixed top-0 w-full h-16 z-20 bg-white max-w-lg mx-auto">
        <Navbar fluid className="h-16 flex items-center border-b border-gray-200">
          <Navbar.Brand as={Link} to="/dashboard">
            <span className="text-lg font-semibold whitespace-nowrap">
              Recount
            </span>
          </Navbar.Brand>
        </Navbar>
      </div>

      <main className="container max-w-lg mx-auto">
        {children}
      </main>

      {/* button navigation */}
      <div class="fixed z-50 w-full h-16 max-w-lg -translate-x-1/2 bg-white border-t border-gray-200 bottom-0 left-1/2 mx-auto">
        <div class="grid h-full max-w-lg grid-cols-5 mx-auto">
            {/* dashboard */}
            <button 
              data-tooltip-target="tooltip-home" 
              type="button" 
              class="inline-flex flex-col items-center justify-center px-5 dark:hover:bg-gray-800 group"
              onClick={() => navigate('/dashboard')}
            >
                <svg class="w-5 h-5 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-pink-600 dark:group-hover:text-pink-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="m19.707 9.293-2-2-7-7a1 1 0 0 0-1.414 0l-7 7-2 2a1 1 0 0 0 1.414 1.414L2 10.414V18a2 2 0 0 0 2 2h3a1 1 0 0 0 1-1v-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v4a1 1 0 0 0 1 1h3a2 2 0 0 0 2-2v-7.586l.293.293a1 1 0 0 0 1.414-1.414Z"/>
                </svg>
                <span class="sr-only">Dashboard</span>
            </button>
            <div id="tooltip-home" role="tooltip" class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-xs opacity-0 tooltip dark:bg-gray-700">
                Dashboard
                <div class="tooltip-arrow" data-popper-arrow></div>
            </div>

            {/* archive */}
            <button 
              data-tooltip-target="tooltip-archive" 
              type="button" 
              class="inline-flex flex-col items-center justify-center px-5 dark:hover:bg-gray-800 group"
              onClick={() => navigate('/archive')}
            >
                <svg class="w-5 h-5 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-pink-600 dark:group-hover:text-pink-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 6a2 2 0 0 1 2-2h5.532a2 2 0 0 1 1.536.72l1.9 2.28H3V6Zm0 3v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9H3Z" clip-rule="evenodd"/>
                </svg>
                <span class="sr-only">Archive</span>
            </button>
            <div id="tooltip-archive" role="tooltip" class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-xs opacity-0 tooltip dark:bg-gray-700">
                Archive
                <div class="tooltip-arrow" data-popper-arrow></div>
            </div>

            {/* new */}
            <div class="flex items-center justify-center">
                <button 
                  data-tooltip-target="tooltip-new" 
                  type="button" 
                  class="inline-flex items-center justify-center w-10 h-10 font-medium bg-pink-600 rounded-full hover:bg-pink-700 group focus:ring-4 focus:ring-pink-300 focus:outline-none dark:focus:ring-pink-800"
                  onClick={() => navigate('/dialogue/text')}
                >
                    <svg class="w-4 h-4 text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 18">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 1v16M1 9h16"/>
                    </svg>
                    <span class="sr-only">New</span>
                </button>
            </div>
            <div id="tooltip-new" role="tooltip" class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-xs opacity-0 tooltip dark:bg-gray-700">
                New
                <div class="tooltip-arrow" data-popper-arrow></div>
            </div>

            {/* resource */}
            <button 
              data-tooltip-target="tooltip-resource" 
              type="button" 
              class="inline-flex flex-col items-center justify-center px-5 dark:hover:bg-gray-800 group"
              onClick={() => navigate('/resources')}
            >
                <svg class="w-5 h-5 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-pink-600 dark:group-hover:text-pink-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6 2a2 2 0 0 0-2 2v15a3 3 0 0 0 3 3h12a1 1 0 1 0 0-2h-2v-2h2a1 1 0 0 0 1-1V4a2 2 0 0 0-2-2h-8v16h5v2H7a1 1 0 1 1 0-2h1V2H6Z" clip-rule="evenodd"/>
                </svg>
                <span class="sr-only">Resource</span>
            </button>
            <div id="tooltip-resource" role="tooltip" class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-xs opacity-0 tooltip dark:bg-gray-700">
                Resource
                <div class="tooltip-arrow" data-popper-arrow></div>
            </div>

            {/* profile */}
            <button 
              data-tooltip-target="tooltip-profile" 
              type="button" 
              class="inline-flex flex-col items-center justify-center px-5 dark:hover:bg-gray-800 group"
              onClick={() => {
                logout();
                navigate('/');
              }}
            >
                <svg class="w-5 h-5 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-pink-600 dark:group-hover:text-pink-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                </svg>
                <span class="sr-only">Profile</span>
            </button>
            <div id="tooltip-profile" role="tooltip" class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-xs opacity-0 tooltip dark:bg-gray-700">
                Profile
                <div class="tooltip-arrow" data-popper-arrow></div>
            </div>
        </div>
      </div>

    </div>
  );
};

export default MainLayout; 
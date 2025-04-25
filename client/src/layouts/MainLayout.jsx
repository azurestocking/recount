import React from 'react';
import { Navbar, Button, Avatar, Dropdown, Badge } from 'flowbite-react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const MainLayout = ({ children }) => {
  const { user, logout, isGuest } = useAuth();
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar fluid>
        <Navbar.Brand as={Link} to="/dashboard">
          <img
            src="/logo.svg"
            className="h-8 mr-3"
            alt="Recount Logo"
          />
          <span className="self-center text-xl font-semibold whitespace-nowrap">
            Recount
          </span>
        </Navbar.Brand>
        <div className="flex md:order-2 items-center gap-4">
          {user ? (
            <div className="flex items-center gap-2">
              {isGuest() && (
                <Badge color="info" className="mr-2">
                  Guest Mode
                </Badge>
              )}
              <Dropdown
                arrowIcon={false}
                inline
                label={
                  <Avatar 
                    alt="User" 
                    img={user.avatar || "https://flowbite.com/docs/images/people/profile-picture-5.jpg"} 
                    rounded
                    size="sm"
                  />
                }
              >
                <Dropdown.Header>
                  <span className="block text-sm">
                    {user.name || 'User'}
                  </span>
                  <span className="block truncate text-sm font-medium">
                    {user.email || user.id}
                  </span>
                </Dropdown.Header>
                <Dropdown.Item as={Link} to="/dashboard">
                  Dashboard
                </Dropdown.Item>
                <Dropdown.Item as={Link} to="/timeline">
                  Timeline
                </Dropdown.Item>
                <Dropdown.Item as={Link} to="/resources">
                  Resources
                </Dropdown.Item>
                <Dropdown.Divider />
                <Dropdown.Item onClick={logout}>
                  Sign out
                </Dropdown.Item>
              </Dropdown>
            </div>
          ) : (
            <Button as={Link} to="/login">
              Login
            </Button>
          )}
          <Navbar.Toggle />
        </div>
        <Navbar.Collapse>
          <Navbar.Link as={Link} to="/dashboard" active={isActive('/dashboard')}>
            Dashboard
          </Navbar.Link>
          <Navbar.Link as={Link} to="/resources" active={isActive('/resources')}>
            Resources
          </Navbar.Link>
          <Navbar.Link as={Link} to="/timeline" active={isActive('/timeline')}>
            Timeline
          </Navbar.Link>
        </Navbar.Collapse>
      </Navbar>

      <main className="container mx-auto py-8">
        {children}
      </main>

      <footer className="bg-white border-t">
        <div className="container mx-auto py-4 px-4 text-center text-sm text-gray-500">
          <p>© {new Date().getFullYear()} Recount. All rights reserved.</p>
          <p className="mt-2">
            Disclaimer: This is not a substitute for professional legal advice.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout; 
import React from 'react';
import { Navbar, Button } from 'flowbite-react';

const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar fluid>
        <Navbar.Brand href="/">
          <img
            src="/logo.svg"
            className="h-8 mr-3"
            alt="Recount Logo"
          />
          <span className="self-center text-xl font-semibold whitespace-nowrap">
            Recount
          </span>
        </Navbar.Brand>
        <div className="flex md:order-2">
          <Button>
            Get Started
          </Button>
          <Navbar.Toggle />
        </div>
        <Navbar.Collapse>
          <Navbar.Link href="/" active>
            Home
          </Navbar.Link>
          <Navbar.Link href="/resources">
            Resources
          </Navbar.Link>
          <Navbar.Link href="/timeline">
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
import React from 'react';
import { Button, Card, TextInput } from 'flowbite-react';

const Login = () => {
  return (
    <Card className="max-w-sm mx-auto">
      <h5 className="text-2xl font-bold text-center mb-4">Welcome to Recount</h5>
      <div className="space-y-4">
        <TextInput
          type="email"
          placeholder="Email"
          required
        />
        <TextInput
          type="password"
          placeholder="Password"
          required
        />
        <Button className="w-full">
          Log In
        </Button>
        <div className="text-center">
          <span className="text-sm text-gray-500">or</span>
        </div>
        <div className="flex gap-2">
          <Button color="light" className="w-full">
            Google
          </Button>
          <Button color="light" className="w-full">
            Apple
          </Button>
          <Button color="light" className="w-full">
            Facebook
          </Button>
        </div>
        <Button color="light" className="w-full">
          Continue as guest
        </Button>
      </div>
    </Card>
  );
};

export default Login; 
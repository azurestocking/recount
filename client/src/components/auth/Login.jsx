import React, { useState } from 'react';
import { Button, TextInput, Alert, Label } from 'flowbite-react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const Login = ({ onSignupClick }) => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [credentials, setCredentials] = useState({
    email: '',
    user_password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(credentials.email, credentials.user_password);
      login(response.data.user, response.data.token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGuestLogin = () => {
    const guestUser = {
      id: 'guest-' + Date.now(),
      name: 'Guest User',
      role: 'guest'
    };
    login(guestUser);
    navigate('/dashboard');
  };

  return (
    <div>
      {error && (
        <Alert color="failure" className="mb-4">
          {error}
        </Alert>
      )}
      <form onSubmit={handleLogin} className="flex max-w-md flex-col gap-4">
        <div>
          <div className="mb-2 block">
            <Label htmlFor="email" value="Email" />
          </div>
          <TextInput
            id="email"
            type="email"
            name="email"
            placeholder="Email"
            value={credentials.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <div className="mb-2 block">
            <Label htmlFor="user_password" value="Password" />
          </div>
          <TextInput
            id="user_password"
            type="password"
            name="user_password"
            placeholder="Password"
            value={credentials.user_password}
            onChange={handleChange}
            required
          />
        </div>

        <div className="flex flex-col gap-2 items-center w-full">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Logging in...' : 'Log In'}
          </Button>
          <Button color="light" className="w-full" onClick={handleGuestLogin}>
            Continue as Guest
          </Button>
        </div>


        {/* Divider */}
        <div className="flex items-center w-full">
          <div className="flex-1 border-t border-gray-200"></div>
          <span className="px-2 text-sm font-normal text-gray-500">OR LOGIN WITH</span>
          <div className="flex-1 border-t border-gray-200"></div>
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

        <div className="text-sm font-normal text-center w-full">
          <span className="text-gray-500">Don't have an account? </span>
          <button className="text-pink-700 ml-1 hover:underline" onClick={onSignupClick}>
            Sign Up Now
          </button>
        </div>
      </form>
    </div>
  );
};

export default Login; 
import React, { useState } from 'react';
import { Button, Card, TextInput, Alert } from 'flowbite-react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [credentials, setCredentials] = useState({
    user_account: '',
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
      const response = await authAPI.login(credentials.user_account, credentials.user_password);
      login(response.data.user, response.data.token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGuestLogin = () => {
    // For demo purposes, create a guest user
    const guestUser = {
      id: 'guest-' + Date.now(),
      name: 'Guest User',
      role: 'guest'
    };
    login(guestUser);
    // Directly navigate to dashboard
    navigate('/dashboard');
  };

  return (
    <Card className="max-w-sm mx-auto mt-10">
      <h5 className="text-2xl font-bold text-center mb-4">Welcome to Recount</h5>
      {error && (
        <Alert color="failure" className="mb-4">
          {error}
        </Alert>
      )}
      <form onSubmit={handleLogin} className="space-y-4">
        <TextInput
          type="text"
          name="user_account"
          placeholder="Account"
          value={credentials.user_account}
          onChange={handleChange}
          required
        />
        <TextInput
          type="password"
          name="user_password"
          placeholder="Password"
          value={credentials.user_password}
          onChange={handleChange}
          required
        />
        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Logging in...' : 'Log In'}
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
        <Button color="light" className="w-full" onClick={handleGuestLogin}>
          Continue as guest
        </Button>
      </form>
    </Card>
  );
};

export default Login; 
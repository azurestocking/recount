import React, { useState } from 'react';
import { Button, Card, TextInput, Alert } from 'flowbite-react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const Signup = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [userData, setUserData] = useState({
    user_name: '',
    user_account: '',
    user_password: '',
    email: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      console.log('Attempting to register with data:', userData);
      const response = await authAPI.register(userData);
      console.log('Registration response:', response);
      
      if (response.data) {
        login(response.data.user, response.data.token);
        navigate('/dashboard');
      } else {
        setError('Registration failed: No response data received');
      }
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.response?.data?.detail || err.message || 'Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="max-w-sm mx-auto mt-10">
      <h5 className="text-2xl font-bold text-center mb-4">Sign Up for Recount</h5>
      {error && (
        <Alert color="failure" className="mb-4">
          {error}
        </Alert>
      )}
      <form onSubmit={handleSignup} className="space-y-4">
        <TextInput
          type="text"
          name="user_name"
          placeholder="Full Name"
          value={userData.user_name}
          onChange={handleChange}
          required
        />
        <TextInput
          type="text"
          name="user_account"
          placeholder="Username"
          value={userData.user_account}
          onChange={handleChange}
          required
        />
        <TextInput
          type="password"
          name="user_password"
          placeholder="Password"
          value={userData.user_password}
          onChange={handleChange}
          required
        />
        <TextInput
          type="email"
          name="email"
          placeholder="Email"
          value={userData.email}
          onChange={handleChange}
          required
        />
        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Signing up...' : 'Sign Up'}
        </Button>
      </form>
    </Card>
  );
};

export default Signup; 
import React, { useState } from 'react';
import { Button, TextInput, Alert, Label } from 'flowbite-react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const Signup = ({ onLoginClick }) => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [userData, setUserData] = useState({
    user_name: '',
    email: '',
    user_password: '',
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
      const response = await authAPI.register(userData);
      if (response.data) {
        login(response.data.user, response.data.token);
        navigate('/dashboard');
      } else {
        setError('Registration failed: No response data received');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {error && (
        <Alert color="failure" className="mb-4">
          {error}
        </Alert>
      )}
      <form onSubmit={handleSignup} className="flex max-w-md flex-col gap-4">
        <div>
          <div className="mb-2 block">
            <Label htmlFor="user_name" value="Name" />
          </div>
          <TextInput
            id="user_name"
            type="text"
            name="user_name"
            placeholder="Full Name"
            value={userData.user_name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <div className="mb-2 block">
            <Label htmlFor="email" value="Email" />
          </div>
          <TextInput
            id="email"
            type="email"
            name="email"
            placeholder="Email"
            value={userData.email}
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
            value={userData.user_password}
            onChange={handleChange}
            required
          />
        </div>

        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Signing up...' : 'Sign Up'}
        </Button>

        <div className="text-sm font-normal text-center w-full">
          <span className="text-gray-500">Already have an account? </span>
          <button className="text-pink-700 ml-1 hover:underline" onClick={onLoginClick}>
            Log In Now
          </button>
        </div>
      </form>
    </div>
  );
};

export default Signup; 
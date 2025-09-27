/**
 * Example Lynx JS client code for authenticating with the Django backend
 * 
 * This file demonstrates how to use the authentication API endpoints
 * from a Lynx JS mobile application.
 */

// API base URL - adjust for your environment
// For Android emulator
const API_BASE_URL = 'http://10.0.2.2:8000/api/';
// For iOS simulator
// const API_BASE_URL = 'http://localhost:8000/api/';
// For production
// const API_BASE_URL = 'https://your-production-domain.com/api/';

/**
 * Utility function to make authenticated API requests
 * @param {string} endpoint - API endpoint path
 * @param {Object} options - Fetch options
 * @returns {Promise} - Fetch promise
 */
export const fetchWithToken = async (endpoint, options = {}) => {
  // Get token from local storage
  const token = await localStorage.getItem('userToken');
  
  // Set up headers with content type and authorization if token exists
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }
  
  // Configure fetch request
  const config = {
    ...options,
    headers,
  };
  
  // Make the API request
  return fetch(`${API_BASE_URL}${endpoint}`, config);
};

/**
 * Register a new user
 * @param {string} username - User's username
 * @param {string} email - User's email
 * @param {string} password - User's password
 * @param {string} password2 - Password confirmation
 * @returns {Promise} - Registration result
 */
export const register = async (username, email, password, password2) => {
  try {
    const response = await fetch(`${API_BASE_URL}auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        email,
        password,
        password2,
      }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Registration failed');
    }
    
    // Store token in local storage
    if (data.token) {
      await localStorage.setItem('userToken', data.token);
    }
    
    return data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

/**
 * Log in a user
 * @param {string} username - User's username
 * @param {string} password - User's password
 * @returns {Promise} - Login result
 */
export const login = async (username, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Login failed');
    }
    
    // Store token in local storage
    if (data.token) {
      await localStorage.setItem('userToken', data.token);
    }
    
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

/**
 * Log out the current user
 * @returns {Promise} - Logout result
 */
export const logout = async () => {
  try {
    const response = await fetchWithToken('auth/logout/', {
      method: 'POST',
    });
    
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || 'Logout failed');
    }
    
    // Remove token from local storage
    await localStorage.removeItem('userToken');
    
    return { success: true };
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
};

/**
 * Get the current user's profile
 * @returns {Promise} - User profile data
 */
export const getUserProfile = async () => {
  try {
    const response = await fetchWithToken('auth/profile/');
    
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || 'Failed to get user profile');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Get profile error:', error);
    throw error;
  }
};

/**
 * Validate the current authentication token
 * @returns {Promise} - Token validation result
 */
export const validateToken = async () => {
  try {
    const token = await localStorage.getItem('userToken');
    
    if (!token) {
      return { isValid: false };
    }
    
    const response = await fetchWithToken('auth/validate-token/');
    
    if (!response.ok) {
      // If token is invalid, remove it from storage
      await localStorage.removeItem('userToken');
      return { isValid: false };
    }
    
    const data = await response.json();
    return { isValid: true, user: data.user };
  } catch (error) {
    console.error('Token validation error:', error);
    // On error, assume token is invalid
    await localStorage.removeItem('userToken');
    return { isValid: false };
  }
};

/**
 * Example of how to use these functions in a Lynx JS React component
 */
/*
import React, { useState, useEffect } from '@lynx-js/react';
import { View, Text, TextInput, Button } from '@lynx-js/core';
import { login, register, logout, getUserProfile, validateToken } from './api';

const AuthExample = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Check if user is already logged in on component mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        setLoading(true);
        const { isValid, user } = await validateToken();
        if (isValid && user) {
          setUser(user);
        }
      } catch (err) {
        console.error('Auth check error:', err);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogin = async () => {
    try {
      setError('');
      setLoading(true);
      const data = await login(username, password);
      setUser(data.user);
    } catch (err) {
      setError('Login failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      setLoading(true);
      await logout();
      setUser(null);
    } catch (err) {
      setError('Logout failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={{ padding: 20 }}>
      {user ? (
        <View>
          <Text style={{ fontSize: 18, marginBottom: 20 }}>
            Welcome, {user.username}!
          </Text>
          <Button title="Logout" onPress={handleLogout} />
        </View>
      ) : (
        <View>
          <Text style={{ fontSize: 24, marginBottom: 20 }}>Login</Text>
          {error ? <Text style={{ color: 'red' }}>{error}</Text> : null}
          <TextInput
            placeholder="Username"
            value={username}
            onChangeText={setUsername}
            style={{ marginBottom: 10, padding: 10, borderWidth: 1 }}
          />
          <TextInput
            placeholder="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            style={{ marginBottom: 20, padding: 10, borderWidth: 1 }}
          />
          <Button title="Login" onPress={handleLogin} />
        </View>
      )}
    </View>
  );
};

export default AuthExample;
*/
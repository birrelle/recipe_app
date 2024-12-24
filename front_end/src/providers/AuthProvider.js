import React, { useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import authService from '../services/authService';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    try {
      const data = await authService.login(email, password);

      if (data.ok) {
        setUser(data.user);
        return { success: true, user: data.user };
      } else {
        return { success: false, error: data.message };
      }
    } catch (error) {
      return { 
        success: false, 
        error: 'Network error. Please try again.' 
      };
    }
  };

  const logout = async () => {
    try {
      const data = await authService.logout();

      if (data.ok) {
        setUser(null);
        return { success: true };
      }
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  const register = async (email, password) => {
    try {
      const data = await authService.register(email, password);

      if (data.ok) {
        return { success: true, userId: data.user_id };
      } else {
        return { success: false, error: data.message };
      }
    } catch (error) {
      return { 
        success: false, 
        error: 'Registration failed. Please try again.' 
      };
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};
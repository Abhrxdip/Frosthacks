import { useState } from 'react';
import api from '@/utils/api';

interface LoginData {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  confirmPassword: string;
}

export const useAuth = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = async (data: LoginData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/auth/login', data);
      const { token } = response.data;
      localStorage.setItem('authToken', token);
      return { success: true, token };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Invalid credentials. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    setLoading(true);
    setError(null);
    
    if (data.password !== data.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return { success: false, error: 'Passwords do not match' };
    }

    try {
      const response = await api.post('/auth/register', {
        email: data.email,
        password: data.password,
      });
      const { token } = response.data;
      localStorage.setItem('authToken', token);
      return { success: true, token };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Registration failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    window.location.href = '/login';
  };

  return { login, register, logout, loading, error };
};

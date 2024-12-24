import api from './api';

const authService = {
    login: async (email, password) => {
        try {
            const response = await api.post('/auth/login', { email, password });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : new Error('Login failed');
        }
    },

    register: async (email, password) => {
        try {
            const response = await api.post('/auth/register', { email, password });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : new Error('Registration failed');
        }
    },

    logout: async () => {
        try {
            const response = await api.post('/auth/logout');
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : new Error('Logout failed');
        }
    },

    // Connection test method
    testConnection: async () => {
        try {
            const response = await api.get('/ping');
            return response.status === 200;
        } catch (error) {
            console.error('Backend connection test failed', error);
            return false;
        }
    }
};

export default authService;
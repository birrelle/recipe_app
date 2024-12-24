import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error.response ? error.response.data : error.message);
        
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // Redirect to login or refresh token
                    window.location.href = '/login';
                    break;
                case 403:
                    // Handle forbidden access
                    break;
                case 500:
                    // Handle server errors
                    break;
            }
        }
        
        return Promise.reject(error);
    }
);

export default api;
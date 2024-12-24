// src/App.js
import React from 'react';
import Home from './components/Home';
import './App.css';
import LoginPage from './components/LoginPage';
import { AuthProvider } from './providers/AuthProvider';
import { BrowserRouter,Navigate, Routes, Route } from 'react-router-dom';
import RegisterPage from './components/RegisterPage';
import { useAuth } from './hooks/useAuth';

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

function App() {
  return (
    <div className="app flex flex-col min-h-screen">
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route 
              path="/home" 
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              } 
            />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </div>

    
  );
}

export default App;


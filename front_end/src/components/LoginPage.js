import React, { useState} from 'react';
import { Button, Description, Dialog, DialogPanel, DialogTitle, Input } from '@headlessui/react'
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';


// Login Component
const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [response, setResponse] = useState('');

  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await login(email, password);
      
      if (response.success) {
        setResponse(response)
        // Redirect to dashboard or home
        window.location.href = '/home';
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-custom-lightest-blue">
      <div className="w-full max-w-md bg-white drop-shadow-lg  p-10 rounded-lg">
        <div className="text-2xl text-custom-darkblue tracking-wide text-center pb-3">
          <div>Login to Your Account</div>
        </div>
        <div>
          <form onSubmit={handleLogin} className="space-y-4">
            {error && (
             <Dialog 
             open={isOpen} 
             onClose={() => setIsOpen(false)}
             className="fixed inset-0 z-10 overflow-y-auto"
              >
             <div className="flex min-h-screen items-center justify-center text-custom-darkblue">
               <DialogPanel className="fixed inset-0 bg-black opacity-30" />
               
               <div className="relative bg-white rounded-xl p-4 max-w-sm mx-auto">
                 <DialogTitle 
                   className="text-lg font-bold text-red-600"
                 >
                   Login Error
                 </DialogTitle>
                 
                 <Description 
                   className="text-sm text-gray-500 mt-2"
                 >
                   {error}
                 </Description>
                 
                 <button
                   type="button"
                   onClick={() => setIsOpen(false)}
                   className="mt-4 w-full bg-red-500 text-white py-2 rounded-xl hover:bg-red-600"
                 >
                   Close
                 </button>
               </div>
             </div>
           </Dialog>
              // <Alert variant="destructive">
              //   <AlertDescription>{error}</AlertDescription>
              // </Alert>
            )}
            <div>
              <label htmlFor="email" className="block mb-2 text-custom-darkblue">Email</label>
              <Input
                type="email"
                name="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="Enter your email"
                required
                className="w-full border border-custom-lightblue  focus:border-custom-blue focus:shadow-md rounded-lg py-3 px-5 text-sm leading-5 text-custom-darkblue focus:ring-0 outline-none placeholder-custom-lightblue"
              />
            </div>
            <div>
              <label htmlFor="password" className="block mb-2 text-custom-darkblue">Password</label>
              <Input
                type="password"
                name="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Enter your password"
                required
                className="w-full border border-custom-lightblue  focus:border-custom-blue focus:shadow-md rounded-lg py-3 px-5 mb-4 text-sm leading-5 text-custom-darkblue focus:ring-0 outline-none placeholder-custom-lightblue"
              />
            </div>
            <div>
              <Button 
                type="submit" 
                className="w-full border border-custom-darkblue  focus:border-custom-lightblue focus:shadow-md rounded-3xl py-3 px-10 text-md tracking-wide leading-5 text-custom-lightest-blue bg-custom-darkblue focus:ring-0 outline-none placeholder-custom-lightblue"
                disabled={isLoading}
              >
                {isLoading ? 'Logging in...' : 'Login'}
              </Button>
            </div>
            {error && <div className="text-red-500 text-sm mt-1">{error}</div>} 
          </form>
        </div>
        <div className="text-xs text-custom-blue py-3 text-center">
          <div>Don't have an account? Sign up <Link to="/register" className="underline">here</Link></div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;


// // Authentication Context for managing global auth state
// const AuthContext = React.createContext(null);

// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (context === null) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };

// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(null);

//   const login = async (email, password) => {
//     try {
//       const data = await authService.login(email, password);

//       if (data.ok) {
//         setUser(data.user);
//         return { success: true, user: data.user };
//       } else {
//         return { success: false, error: data.message };
//       }
//     } catch (error) {
//       return { 
//         success: false, 
//         error: 'Network error. Please try again.' 
//       };
//     }
//   };

//   const logout = async () => {
//     try {
//       const data = await authService.logout();

//       if (data.ok) {
//         setUser(null);
//         return { success: true };
//       }
//     } catch (error) {
//       console.error('Logout failed', error);
//     }
//   };

//   const register = async (email, password) => {
//     try {
//       const data = await authService.ref  (email, password);

//       if (data.ok) {
//         return { success: true, userId: data.user_id };
//       } else {
//         return { success: false, error: data.message };
//       }
//     } catch (error) {
//       return { 
//         success: false, 
//         error: 'Registration failed. Please try again.' 
//       };
//     }
//   };

//   return (
//     <AuthContext.Provider value={{ user, login, logout, register }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };
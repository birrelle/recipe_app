import React, { useState, useContext, useEffect} from 'react';
import { Button, Description, Dialog, DialogPanel, DialogTitle, Input } from '@headlessui/react'
import authService from '../services/authService';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';


// Register Component
const RegisterPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setPasswordConfirm] = useState('')
  const [passwordsMatch, setPasswordsMatch] = useState(true);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [response, setResponse] = useState('');

  const { register } = useAuth();
  console.log(error)

  useEffect(() => {
    if (confirmPassword) {
      setPasswordsMatch(password === confirmPassword);
    }
  }, [password, confirmPassword]);


  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');

    // Check if passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    // Check password length (optional)
    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    setIsLoading(true);

    try {
      const response = await register(email, password);
      
      if (response.success) {
        // Redirect to dashboard or home
        window.location.href = '/login';
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError('Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-custom-lightest-blue">
      <div className="w-full max-w-md bg-white drop-shadow-lg  p-10 rounded-lg">
        <div className="text-2xl text-custom-darkblue tracking-wide text-center pb-3">
          <div>Create an Account</div>
        </div>
        <div>
          <form onSubmit={handleRegister} className="space-y-4">
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
                   Account Creation Error
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
                className="w-full border border-custom-lightblue  focus:border-custom-blue focus:shadow-md rounded-lg py-3 px-5  text-sm leading-5 text-custom-darkblue focus:ring-0 outline-none placeholder-custom-lightblue"
              />
            </div>
            <div>
              <label htmlFor="confirmPasswordpassword" className="block mb-2 text-custom-darkblue">Confirm Password</label>
              <Input
                type="password"
                name="confirmPassword"
                value={confirmPassword}
                onChange={(event) => setPasswordConfirm(event.target.value)}
                placeholder="Confirm your password"
                required
                className="w-full border border-custom-lightblue  focus:border-custom-blue focus:shadow-md rounded-lg py-3 px-5 mb-4 text-sm leading-5 text-custom-darkblue focus:ring-0 outline-none placeholder-custom-lightblue"
              />
              {confirmPassword && !passwordsMatch && (
                <p className="text-red-500 text-sm mt-1">
                  Passwords do not match
                </p>
              )}
            </div>
            <div>
              <Button 
                type="submit" 
                className="w-full border border-custom-darkblue  focus:border-custom-lightblue focus:shadow-md rounded-3xl py-3 px-10 text-md tracking-wide leading-5 text-custom-lightest-blue bg-custom-darkblue focus:ring-0 outline-none placeholder-custom-lightblue"
                disabled={isLoading}
              >
                {isLoading ? 'Creating account...' : 'Register'}
              </Button>
            </div>
            {error && <div className="text-red-500 text-sm mt-1">{error}</div>} 
          </form>
        </div>
        <div className="text-xs text-custom-blue py-3 text-center">
          <div>Already have an account? <Link to="/login" className='underline'>Login</Link></div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
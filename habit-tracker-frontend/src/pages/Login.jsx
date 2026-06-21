import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { signInWithGoogle } from '../firebase';
import { Flame } from 'lucide-react';

const Login = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (currentUser) {
      navigate('/');
    }
  }, [currentUser, navigate]);

  const handleGoogleSignIn = async () => {
    try {
      await signInWithGoogle();
      // On success, useEffect will trigger navigation
    } catch (error) {
      console.error("Sign in failed", error);
      alert("Failed to sign in. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-xl p-8 text-center border border-gray-100">
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 bg-emerald-100 rounded-2xl flex items-center justify-center rotate-3">
            <Flame size={48} className="text-emerald-500 fill-emerald-500" />
          </div>
        </div>
        <h1 className="text-3xl font-extrabold text-gray-900 mb-2 tracking-tight">Habit Tracker</h1>
        <p className="text-gray-500 mb-8">Build better habits, one day at a time.</p>
        
        <button 
          onClick={handleGoogleSignIn}
          className="w-full flex items-center justify-center gap-3 bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 px-6 py-4 rounded-xl font-bold transition-all shadow-sm hover:shadow active:scale-95"
        >
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" className="w-6 h-6" />
          Continue with Google
        </button>
      </div>
    </div>
  );
};

export default Login;

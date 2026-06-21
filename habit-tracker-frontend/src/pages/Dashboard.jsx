import React, { useState, useEffect } from 'react';
import api from '../api/axiosInstance';
import HabitCard from '../components/HabitCard';
import AddHabitModal from '../components/AddHabitModal';
import { Plus, LogOut, Loader2 } from 'lucide-react';
import { logout } from '../firebase';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const [habits, setHabits] = useState([]);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const { currentUser } = useAuth();

  const fetchHabits = async () => {
    try {
      const response = await api.get('/habits');
      setHabits(response.data);
    } catch (error) {
      console.error("Failed to fetch habits", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  const handleAddHabit = async (habitData) => {
    try {
      await api.post('/habits', habitData);
      fetchHabits();
    } catch (error) {
      console.error("Failed to add habit", error);
      alert("Failed to create habit.");
    }
  };

  const handleCheckToday = async (id, isChecking) => {
    try {
      // Optimistic update
      setHabits(prev => prev.map(h => {
        if (h.id === id) {
          return { ...h, completed_today: isChecking, current_streak: isChecking ? h.current_streak + 1 : Math.max(0, h.current_streak - 1) };
        }
        return h;
      }));

      const today = new Date().toISOString().split('T')[0];
      
      if (isChecking) {
        await api.post(`/habits/${id}/logs`, { date: today, completed: true });
      } else {
        // Find today's log and delete it or mark incomplete
        // Since the backend might not have a delete log easily exposed in requirements, 
        // we will fetch habits again to ensure sync if error
        await api.post(`/habits/${id}/logs`, { date: today, completed: false });
      }
    } catch (error) {
      console.error("Failed to toggle habit", error);
      fetchHabits(); // Revert optimistic update
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <header className="bg-white border-b border-gray-100 sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 font-bold text-lg overflow-hidden">
              {currentUser?.photoURL ? (
                <img src={currentUser.photoURL} alt="Avatar" className="w-full h-full object-cover" />
              ) : (
                currentUser?.email?.charAt(0).toUpperCase()
              )}
            </div>
            <div>
              <p className="text-xs font-semibold tracking-wider text-gray-500 uppercase">Welcome back</p>
              <h1 className="text-xl font-bold text-gray-900 leading-tight">My Habits</h1>
            </div>
          </div>
          <button 
            onClick={logout}
            className="p-2 text-gray-400 hover:text-gray-700 transition-colors"
            title="Log out"
          >
            <LogOut size={20} />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-4 pt-6">
        {isLoading ? (
          <div className="flex justify-center items-center py-20">
            <Loader2 className="animate-spin text-emerald-500" size={32} />
          </div>
        ) : habits.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200">
            <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-300">
              <Plus size={32} />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-1">No habits yet</h3>
            <p className="text-gray-500 text-sm mb-6 max-w-xs mx-auto">Get started by creating your first habit to track.</p>
            <button 
              onClick={() => setIsAddModalOpen(true)}
              className="bg-emerald-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-emerald-700 transition-colors inline-flex items-center gap-2"
            >
              <Plus size={18} />
              Create Habit
            </button>
          </div>
        ) : (
          <div className="grid gap-3">
            {habits.map(habit => (
              <HabitCard 
                key={habit.id} 
                habit={habit} 
                onCheckToday={handleCheckToday} 
              />
            ))}
          </div>
        )}
      </main>

      {/* FAB (Floating Action Button) */}
      {habits.length > 0 && (
        <button
          onClick={() => setIsAddModalOpen(true)}
          className="fixed bottom-6 right-6 lg:right-auto lg:left-1/2 lg:ml-80 w-14 h-14 bg-emerald-600 text-white rounded-full shadow-lg shadow-emerald-600/30 flex items-center justify-center hover:scale-105 hover:bg-emerald-700 transition-all active:scale-95"
        >
          <Plus size={28} />
        </button>
      )}

      <AddHabitModal 
        isOpen={isAddModalOpen} 
        onClose={() => setIsAddModalOpen(false)}
        onSubmit={handleAddHabit}
      />
    </div>
  );
};

export default Dashboard;

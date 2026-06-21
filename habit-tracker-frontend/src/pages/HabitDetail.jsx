import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/axiosInstance';
import ProgressChart from '../components/ProgressChart';
import StreakBadge from '../components/StreakBadge';
import LogHabitModal from '../components/LogHabitModal';
import BackfillModal from '../components/BackfillModal';
import { ArrowLeft, Check, CalendarPlus, Loader2 } from 'lucide-react';

const HabitDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [habit, setHabit] = useState(null);
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLogModalOpen, setIsLogModalOpen] = useState(false);
  const [isBackfillModalOpen, setIsBackfillModalOpen] = useState(false);

  const fetchHabitData = async () => {
    try {
      // Backend routes usually have GET /habits to list them all.
      // If there's a specific GET /habits/:id, we use it. Let's assume we can fetch all and find it, or there is an endpoint.
      // Based on typical REST, we assume GET /habits/{id}/logs and GET /habits exist or we can find it from the list.
      const [habitsRes, logsRes] = await Promise.all([
        api.get('/habits'),
        api.get(`/habits/${id}/logs`)
      ]);
      
      const foundHabit = habitsRes.data.find(h => h.id.toString() === id);
      if (!foundHabit) {
        navigate('/');
        return;
      }
      setHabit(foundHabit);
      setLogs(logsRes.data);
    } catch (error) {
      console.error("Failed to fetch habit details", error);
      alert("Failed to load habit details");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHabitData();
  }, [id]);

  const handleLogSubmit = async (logData) => {
    try {
      await api.post(`/habits/${id}/logs`, logData);
      fetchHabitData(); // Refresh data to update streak and logs
    } catch (error) {
      console.error("Failed to add log", error);
      alert("Failed to save record.");
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="animate-spin text-emerald-500" size={32} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <header className="bg-white border-b border-gray-100 sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center gap-4">
          <button 
            onClick={() => navigate('/')}
            className="p-2 -ml-2 text-gray-400 hover:text-gray-900 hover:bg-gray-50 rounded-full transition-colors"
          >
            <ArrowLeft size={24} />
          </button>
          <div className="flex-grow min-w-0 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold tracking-wider text-gray-400 uppercase">{habit.frequency}</p>
              <h1 className="text-xl font-bold text-gray-900 leading-tight truncate">{habit.name}</h1>
            </div>
            <StreakBadge streak={habit.current_streak} />
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 pt-6 space-y-6">
        
        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3">
          <button 
            onClick={() => setIsLogModalOpen(true)}
            disabled={habit.completed_today}
            className={`flex flex-col items-center justify-center p-4 rounded-2xl border transition-all ${
              habit.completed_today 
                ? 'bg-gray-50 border-gray-200 text-gray-400 cursor-not-allowed' 
                : 'bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100 hover:border-emerald-300 shadow-sm hover:shadow'
            }`}
          >
            <Check size={28} className="mb-2" />
            <span className="font-semibold text-sm">
              {habit.completed_today ? 'Completed Today' : 'Log Today'}
            </span>
          </button>

          <button 
            onClick={() => setIsBackfillModalOpen(true)}
            className="flex flex-col items-center justify-center p-4 rounded-2xl bg-white border border-indigo-100 text-indigo-600 hover:bg-indigo-50 hover:border-indigo-200 transition-all shadow-sm hover:shadow"
          >
            <CalendarPlus size={28} className="mb-2" />
            <span className="font-semibold text-sm">Backfill Past</span>
          </button>
        </div>

        {/* Chart */}
        <div>
          <ProgressChart data={logs.slice(0, 30).reverse()} />
        </div>

        {/* History List */}
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-4 ml-1">History</h3>
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            {logs.length === 0 ? (
              <p className="p-8 text-center text-gray-500">No records yet.</p>
            ) : (
              <ul className="divide-y divide-gray-50">
                {logs.map((log) => (
                  <li key={log.id} className="p-4 flex items-center justify-between hover:bg-gray-50/50 transition-colors">
                    <div>
                      <p className="font-medium text-gray-900">
                        {new Date(log.date).toLocaleDateString('en-US', { weekday: 'short', month: 'long', day: 'numeric', year: 'numeric' })}
                      </p>
                      {log.notes && <p className="text-sm text-gray-500 mt-0.5">{log.notes}</p>}
                    </div>
                    <div>
                      {log.completed ? (
                        <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full">
                          <Check size={12} />
                          Done
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-xs font-semibold text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full">
                          Missed
                        </span>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>

      <LogHabitModal 
        isOpen={isLogModalOpen} 
        onClose={() => setIsLogModalOpen(false)} 
        onSubmit={handleLogSubmit} 
      />
      
      <BackfillModal 
        isOpen={isBackfillModalOpen} 
        onClose={() => setIsBackfillModalOpen(false)} 
        onSubmit={handleLogSubmit} 
      />
    </div>
  );
};

export default HabitDetail;

import React from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle2, Circle, ChevronRight } from 'lucide-react';
import StreakBadge from './StreakBadge';

const HabitCard = ({ habit, onCheckToday }) => {
  return (
    <div className="group relative bg-white rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 border border-gray-100 overflow-hidden flex items-center p-4 gap-4">
      
      {/* Check Button */}
      <button 
        onClick={(e) => {
          e.preventDefault();
          onCheckToday(habit.id, !habit.completed_today);
        }}
        className="flex-shrink-0 focus:outline-none focus:ring-2 focus:ring-emerald-500 rounded-full transition-transform active:scale-95"
      >
        {habit.completed_today ? (
          <CheckCircle2 size={32} className="text-emerald-500 fill-emerald-50" />
        ) : (
          <Circle size={32} className="text-gray-300 hover:text-emerald-400 transition-colors" />
        )}
      </button>

      {/* Habit Info */}
      <div className="flex-grow min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {habit.name}
          </h3>
          <StreakBadge streak={habit.current_streak} />
        </div>
        <p className="text-sm text-gray-500 capitalize">
          {habit.frequency}
        </p>
      </div>

      {/* Details Link */}
      <Link 
        to={`/habits/${habit.id}`}
        className="flex-shrink-0 p-2 text-gray-400 hover:text-gray-900 hover:bg-gray-50 rounded-full transition-colors"
      >
        <ChevronRight size={20} />
      </Link>
    </div>
  );
};

export default HabitCard;

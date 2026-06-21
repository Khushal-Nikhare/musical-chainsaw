import React from 'react';
import { Flame } from 'lucide-react';

const StreakBadge = ({ streak }) => {
  if (!streak || streak === 0) return null;

  return (
    <div className="flex items-center gap-1 bg-orange-100 text-orange-600 px-2 py-1 rounded-full text-xs font-bold shadow-sm">
      <Flame size={14} className="fill-orange-500" />
      <span>{streak} Day{streak !== 1 ? 's' : ''}</span>
    </div>
  );
};

export default StreakBadge;

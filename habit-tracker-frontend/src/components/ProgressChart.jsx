import React from 'react';
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const ProgressChart = ({ data }) => {
  // data should be an array of objects: { date: '2023-10-01', completed: true/false }

  const chartData = data.map(d => ({
    name: new Date(d.date).toLocaleDateString('en-US', { day: 'numeric', month: 'short' }),
    completed: d.completed ? 1 : 0,
    originalDate: d.date,
    status: d.completed
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-2 rounded shadow border border-gray-100 text-sm">
          <p className="font-semibold text-gray-700">{data.name}</p>
          <p className={data.status ? "text-green-600" : "text-gray-400"}>
            {data.status ? 'Completed' : 'Missed'}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="h-64 w-full bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <h3 className="text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wider">30 Day History</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <XAxis 
            dataKey="name" 
            tick={{ fontSize: 10, fill: '#9CA3AF' }} 
            tickLine={false} 
            axisLine={false}
            minTickGap={20}
          />
          <Tooltip content={<CustomTooltip />} cursor={{fill: '#F3F4F6'}} />
          <Bar dataKey="completed" radius={[4, 4, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.status ? '#10B981' : '#E5E7EB'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProgressChart;

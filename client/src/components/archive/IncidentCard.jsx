import React from 'react';

const statusColors = {
  in_progress: 'bg-red-100 text-red-700',
  resolved: 'bg-green-100 text-green-700',
};

const IncidentCard = ({ incident, onClick }) => {
  return (
    <div
      className="border rounded-lg p-4 shadow hover:bg-gray-50 cursor-pointer flex flex-col gap-2"
      onClick={onClick}
    >
      <div className="flex items-center gap-2">
        <span className={`px-2 py-1 rounded text-xs font-semibold ${statusColors[incident.status] || 'bg-gray-100 text-gray-700'}`}>{incident.status === 'resolved' ? 'Resolved' : 'In Progress'}</span>
        <span className="text-sm text-gray-500 ml-auto">{new Date(incident.created_at).toLocaleDateString()}</span>
      </div>
      <div className="font-bold text-lg">{incident.title}</div>
      <div className="text-gray-600 text-sm line-clamp-2">{incident.description}</div>
      <div className="text-xs text-gray-400">Updated {new Date(incident.updated_at).toLocaleString()}</div>
    </div>
  );
};

export default IncidentCard; 
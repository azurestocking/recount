import React from 'react';

const ExhibitList = ({ exhibits }) => {
  if (!exhibits || exhibits.length === 0) {
    return <div className="text-gray-400">No exhibits uploaded.</div>;
  }
  return (
    <div className="space-y-2">
      {exhibits.map(ex => (
        <div key={ex.id} className="border rounded p-2 flex items-center gap-2 bg-gray-50">
          <span className="text-red-600 font-bold">PDF</span>
          <span className="flex-1">{ex.file_path.split('/').pop()}</span>
          <span className="text-xs text-gray-500">{new Date(ex.created_at).toLocaleDateString()}</span>
          {ex.file_path && (
            <a href={ex.file_path} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline ml-2">View</a>
          )}
        </div>
      ))}
    </div>
  );
};

export default ExhibitList; 
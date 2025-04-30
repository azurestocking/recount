import React, { useState } from 'react';
import { addTimelineEvent } from '../../services/api';

const TimelineView = ({ incidentId, timeline, setTimeline }) => {
  const [desc, setDesc] = useState('');
  const [date, setDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const formatDateTime = (dateStr) => {
    const date = new Date(dateStr);
    return {
      fullDate: date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      }),
      time: date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      })
    };
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const newEvent = await addTimelineEvent(incidentId, {
        event_date: new Date(date).toISOString(),
        description: desc,
      });
      setTimeline([...timeline, newEvent]);
      setDesc('');
      setDate('');
    } catch (err) {
      setError('Failed to add event');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form className="flex gap-2 mb-4" onSubmit={handleAdd}>
        <input
          type="datetime-local"
          value={date}
          onChange={e => setDate(e.target.value)}
          className="border rounded px-2 py-1"
          required
        />
        <input
          type="text"
          value={desc}
          onChange={e => setDesc(e.target.value)}
          placeholder="Event description"
          className="border rounded px-2 py-1 flex-1"
          required
        />
        <button type="submit" className="bg-blue-600 text-white px-3 py-1 rounded" disabled={loading}>
          Add
        </button>
      </form>
      {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
      
      {/* Timeline Display */}
      <div className="relative">
        {timeline.length === 0 && <div className="text-gray-400">No events yet.</div>}
        
        {/* Vertical Line */}
        {timeline.length > 0 && (
          <div className="absolute left-[7px] top-2 bottom-2 w-[2px] bg-gray-200" />
        )}

        {/* Timeline Events */}
        <div className="space-y-4">
          {timeline.map(ev => {
            const { fullDate, time } = formatDateTime(ev.event_date);
            return (
              <div key={ev.id} className="relative pl-8">
                {/* Timeline Dot */}
                <div className="absolute left-0 w-4 h-4 rounded-full bg-white border-2 border-gray-300" style={{ top: '2px' }} />
                
                {/* Event Content */}
                <div>
                  <div className="text-sm text-gray-500">{fullDate}</div>
                  <div className="text-sm text-gray-500">{time}</div>
                  <div className="text-gray-700 mt-1">{ev.description}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default TimelineView; 
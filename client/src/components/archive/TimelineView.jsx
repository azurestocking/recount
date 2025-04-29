import React, { useState } from 'react';
import { addTimelineEvent } from '../../services/api';

const TimelineView = ({ incidentId, timeline, setTimeline }) => {
  const [desc, setDesc] = useState('');
  const [date, setDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
      <div className="space-y-2">
        {timeline.length === 0 && <div className="text-gray-400">No events yet.</div>}
        {timeline.map(ev => (
          <div key={ev.id} className="border rounded p-2 bg-gray-50">
            <div className="text-xs text-gray-500 mb-1">{new Date(ev.event_date).toLocaleString()}</div>
            <div>{ev.description}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TimelineView; 
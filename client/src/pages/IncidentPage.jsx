import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getIncident, getTimeline, getExhibits, updateIncident, deleteIncident } from '../services/api';
import TimelineView from '../components/archive/TimelineView';
import ExhibitList from '../components/archive/ExhibitList';
import ChatHistory from '../components/archive/ChatHistory';

const IncidentPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [incident, setIncident] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [exhibits, setExhibits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      getIncident(id),
      getTimeline(id),
      getExhibits(id),
    ])
      .then(([incident, timeline, exhibits]) => {
        setIncident(incident);
        setTimeline(timeline);
        setExhibits(exhibits);
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, [id]);

  // Close menu on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleMarkResolved = async () => {
    try {
      await updateIncident(id, { status: 'resolved' });
      setIncident({ ...incident, status: 'resolved' });
      setMenuOpen(false);
    } catch (e) {
      alert('Failed to mark as resolved.');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this incident?')) return;
    try {
      await deleteIncident(id);
      navigate('/archive');
    } catch (e) {
      alert('Failed to delete incident.');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error || !incident) return <div>Error loading incident.</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-4 flex items-center justify-between">
        <button className="text-blue-600" onClick={() => window.history.back()}>&larr; Back</button>
        {/* Action Menu */}
        <div className="relative" ref={menuRef}>
          <button
            className="p-2 rounded-full hover:bg-gray-100 focus:outline-none"
            onClick={() => setMenuOpen((v) => !v)}
            aria-label="Open actions menu"
          >
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="19" r="1.5"/></svg>
          </button>
          {menuOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded shadow-lg z-10">
              <button className="block w-full text-left px-4 py-2 hover:bg-gray-100" onClick={() => { setMenuOpen(false); alert('Ask AI coming soon!'); }}>Ask AI</button>
              <button className="block w-full text-left px-4 py-2 hover:bg-gray-100" onClick={() => { setMenuOpen(false); alert('Share coming soon!'); }}>Share</button>
              {incident.status !== 'resolved' && (
                <button className="block w-full text-left px-4 py-2 hover:bg-gray-100" onClick={handleMarkResolved}>Mark Resolved</button>
              )}
              <button className="block w-full text-left px-4 py-2 text-red-600 hover:bg-gray-100" onClick={handleDelete}>Delete</button>
            </div>
          )}
        </div>
      </div>
      <div className="flex flex-col md:flex-row gap-8">
        {/* Left: Details & Timeline */}
        <div className="flex-1 min-w-0">
          <div className="mb-6 p-6 bg-white rounded shadow">
            <div className="flex items-center gap-2 mb-2">
              <span className={`px-2 py-1 rounded text-xs font-semibold ${incident.status === 'resolved' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{incident.status === 'resolved' ? 'Resolved' : 'In Progress'}</span>
              <span className="text-sm text-gray-500 ml-auto">{new Date(incident.created_at).toLocaleDateString()}</span>
            </div>
            <div className="font-bold text-2xl mb-1">{incident.title}</div>
            <div className="text-gray-600 mb-1">{incident.description}</div>
            <div className="text-xs text-gray-400">Location: {incident.location || 'N/A'}</div>
          </div>
          <div className="mb-6 p-6 bg-white rounded shadow">
            <h3 className="font-semibold text-lg mb-2">Timeline</h3>
            <TimelineView incidentId={id} timeline={timeline} setTimeline={setTimeline} />
          </div>
        </div>
        {/* Right: Exhibit & Chat */}
        <div className="flex flex-col gap-6 w-full md:w-96">
          <div className="p-6 bg-white rounded shadow">
            <h3 className="font-semibold text-lg mb-2">Exhibit</h3>
            <ExhibitList exhibits={exhibits} />
          </div>
          <div className="p-6 bg-white rounded shadow min-h-[120px] flex flex-col">
            <h3 className="font-semibold text-lg mb-2">Chat History</h3>
            <ChatHistory incidentId={id} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default IncidentPage; 
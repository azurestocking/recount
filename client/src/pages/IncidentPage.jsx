import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getIncident, getTimeline, getExhibits } from '../services/api';
import TimelineView from '../components/archive/TimelineView';
import ExhibitList from '../components/archive/ExhibitList';

const IncidentPage = () => {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [exhibits, setExhibits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) return <div>Loading...</div>;
  if (error || !incident) return <div>Error loading incident.</div>;

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <button className="mb-4 text-blue-600" onClick={() => window.history.back()}>&larr; Back</button>
      <div className="mb-4">
        <div className="flex items-center gap-2">
          <span className={`px-2 py-1 rounded text-xs font-semibold ${incident.status === 'resolved' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{incident.status === 'resolved' ? 'Resolved' : 'In Progress'}</span>
          <span className="text-sm text-gray-500 ml-auto">{new Date(incident.created_at).toLocaleDateString()}</span>
        </div>
        <div className="font-bold text-2xl mt-2">{incident.title}</div>
        <div className="text-gray-600 mt-1">{incident.description}</div>
        <div className="text-xs text-gray-400 mt-1">Location: {incident.location || 'N/A'}</div>
      </div>
      <div className="mb-8">
        <h3 className="font-semibold text-lg mb-2">Timeline</h3>
        <TimelineView incidentId={id} timeline={timeline} setTimeline={setTimeline} />
      </div>
      <div>
        <h3 className="font-semibold text-lg mb-2">Exhibit</h3>
        <ExhibitList exhibits={exhibits} />
      </div>
    </div>
  );
};

export default IncidentPage; 
import React, { useEffect, useState } from 'react';
import { getIncidents } from '../services/api';
import { useNavigate } from 'react-router-dom';
import IncidentCard from '../components/archive/IncidentCard';

const ArchivePage = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    getIncidents()
      .then(setIncidents)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading incidents.</div>;

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Archive</h2>
      <div className="space-y-4">
        {incidents.map(incident => (
          <IncidentCard
            key={incident.id}
            incident={incident}
            onClick={() => navigate(`/archive/incident/${incident.id}`)}
          />
        ))}
      </div>
    </div>
  );
};

export default ArchivePage; 
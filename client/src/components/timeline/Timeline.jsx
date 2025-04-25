import React, { useState, useEffect } from 'react';
import { Card, Spinner, Alert } from 'flowbite-react';
import { chatAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const TimelineItem = ({ time, title, description }) => (
  <div className="mb-8 relative">
    <div className="absolute left-0 w-1 h-full bg-blue-100">
      <div className="absolute left-[-4px] top-2 w-3 h-3 rounded-full bg-blue-600" />
    </div>
    <div className="ml-6">
      <Card>
        <div className="text-sm text-gray-500">{time}</div>
        <h5 className="text-lg font-semibold">{title}</h5>
        {description && (
          <p className="text-gray-700">{description}</p>
        )}
      </Card>
    </div>
  </div>
);

const Timeline = () => {
  const { user, isGuest } = useAuth();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Get user ID from auth context
  const userId = user?.id || 'guest';

  useEffect(() => {
    const fetchTimelineData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // For guest users, show a limited timeline
        if (isGuest()) {
          // Create some sample timeline events for guest users
          const sampleEvents = [
            {
              time: new Date().toLocaleString(),
              title: 'Welcome to Recount',
              description: 'You are using the application in guest mode.'
            },
            {
              time: new Date(Date.now() - 3600000).toLocaleString(),
              title: 'Guest Session Started',
              description: 'Your guest session has been initialized.'
            }
          ];
          setEvents(sampleEvents);
          setLoading(false);
          return;
        }
        
        // For registered users, fetch from API
        // First get user conversations
        const conversationsResponse = await chatAPI.getUserConversations(userId);
        
        if (conversationsResponse.data.conversations && 
            conversationsResponse.data.conversations.length > 0) {
          // Get the most recent conversation
          const mostRecentConversation = conversationsResponse.data.conversations[0];
          
          // Get timeline for this conversation
          const timelineResponse = await chatAPI.getTimeline(mostRecentConversation.id);
          
          if (timelineResponse.data.timeline) {
            setEvents(timelineResponse.data.timeline);
          }
        }
      } catch (err) {
        console.error('Error fetching timeline data:', err);
        setError('Failed to load timeline data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchTimelineData();
  }, [userId, isGuest]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="xl" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-500 p-4">
        {error}
      </div>
    );
  }

  return (
    <div className="relative p-4">
      {isGuest() && (
        <Alert color="info" className="mb-4">
          <span className="font-medium">Guest Mode:</span> You are viewing a limited timeline with sample data.
        </Alert>
      )}
      
      {events.length === 0 ? (
        <div className="text-center text-gray-500">
          No actions recorded yet
        </div>
      ) : (
        events.map((event, index) => (
          <TimelineItem
            key={index}
            time={event.time}
            title={event.title}
            description={event.description}
          />
        ))
      )}
    </div>
  );
};

export default Timeline; 
import React from 'react';
import { Card } from 'flowbite-react';

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

const Timeline = ({ events = [] }) => {
  return (
    <div className="relative p-4">
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
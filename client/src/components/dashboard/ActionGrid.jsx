import React from 'react';
import { Card } from 'flowbite-react';

const ActionCard = ({ title, onClick }) => (
  <Card 
    className="cursor-pointer hover:bg-gray-50 transition-colors"
    onClick={onClick}
  >
    <h5 className="text-lg font-semibold">{title}</h5>
    <div className="flex justify-end">
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </Card>
);

const ActionGrid = () => {
  const actions = [
    { title: 'Document an Incident', handler: () => {} },
    { title: 'Prepare a Police Report', handler: () => {} },
    { title: 'Prepare an Affidavit', handler: () => {} },
    { title: 'Draft a Demand Letter', handler: () => {} },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto p-4">
      {actions.map((action, index) => (
        <ActionCard
          key={index}
          title={action.title}
          onClick={action.handler}
        />
      ))}
      <div className="col-span-full text-center text-sm text-gray-500 mt-4">
        Disclaimer: This information is not substituted by a law professional.
      </div>
    </div>
  );
};

export default ActionGrid; 
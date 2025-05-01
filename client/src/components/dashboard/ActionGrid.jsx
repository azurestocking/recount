import React from 'react';
import { Card } from 'flowbite-react';
import { useNavigate } from 'react-router-dom';

const ActionCard = ({ title, description, onClick }) => (
  <Card 
    className="w-full cursor-pointer hover:bg-gray-50 transition-colors"
    onClick={onClick}
  >
    <div className="flex flex-col gap-2">
      <h5 className="text-lg font-semibold">{title}</h5>
      <p className="text-sm text-gray-500">{description}</p>
    </div>
  </Card>
);

const ActionGrid = () => {
  const navigate = useNavigate();
  
  const actions = [
    { 
      title: 'Document an Incident', 
      description: 'Create a detailed record of what happened, including dates, times, and key details.',
      handler: () => navigate('/dialogue/text')
    },
    { 
      title: 'Prepare an affidavit', 
      description: 'Generate a formal written statement of facts that can be used as evidence in court.',
      handler: () => navigate('/dialogue/text')
    },
    { 
      title: 'Understand my rights', 
      description: 'Learn about your legal rights and available social supports as a survivor of violence.',
      handler: () => navigate('/dialogue/text')
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 w-full">
      {actions.map((action, index) => (
        <ActionCard
          key={index}
          title={action.title}
          description={action.description}
          onClick={action.handler}
        />
      ))}
    </div>
  );
};

export default ActionGrid; 
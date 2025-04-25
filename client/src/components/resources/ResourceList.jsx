import React, { useState } from 'react';
import { Card, TextInput, Tabs } from 'flowbite-react';

const ResourceCard = ({ title, description, readTime }) => (
  <Card className="mb-4">
    <h5 className="text-lg font-semibold">{title}</h5>
    <p className="text-gray-700">{description}</p>
    <div className="flex items-center text-sm text-gray-500">
      <span>{readTime} min read</span>
    </div>
  </Card>
);

const FAQItem = ({ question, answer }) => (
  <Card className="mb-4">
    <h5 className="text-lg font-semibold">{question}</h5>
    <p className="text-gray-700">{answer}</p>
  </Card>
);

const ResourceList = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const articles = [
    {
      title: 'Understanding Your Legal Rights',
      description: 'A comprehensive guide to basic legal rights and protections.',
      readTime: 5
    },
    // Add more articles here
  ];

  const faqs = [
    {
      question: 'What should I do immediately after an incident?',
      answer: 'Document everything, take photos if relevant, and report to authorities if necessary.'
    },
    // Add more FAQs here
  ];

  return (
    <div className="max-w-4xl mx-auto p-4">
      <TextInput
        className="mb-4"
        placeholder="Search resources..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      <Tabs>
        <Tabs.Item title="Articles" active>
          {articles.map((article, index) => (
            <ResourceCard key={index} {...article} />
          ))}
        </Tabs.Item>
        <Tabs.Item title="FAQ">
          {faqs.map((faq, index) => (
            <FAQItem key={index} {...faq} />
          ))}
        </Tabs.Item>
      </Tabs>
    </div>
  );
};

export default ResourceList; 
import { Button, Card } from 'flowbite-react';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-center mb-4">
        Welcome to Recount
      </h1>
      <div className="max-w-sm mx-auto">
        <Card>
          <h5 className="text-2xl font-bold tracking-tight text-gray-900">
            Flowbite Card
          </h5>
          <p className="font-normal text-gray-700">
            This is a Flowbite card component with a button.
          </p>
          <Button>Flowbite Button</Button>
        </Card>
      </div>
    </div>
  );
}

export default App; 
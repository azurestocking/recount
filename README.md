# Recount - Legal Assistant AI Agent

## Project Structure

```
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── features/      # Feature-specific components and logic
│   │   ├── layouts/       # Layout components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API and external services
│   │   ├── store/        # State management
│   │   ├── styles/       # Global styles and theme
│   │   └── utils/        # Utility functions and helpers
│   └── public/           # Static assets
│
└── server/               # Backend application
    ├── src/
    │   ├── controllers/  # Request handlers
    │   ├── models/       # Data models
    │   ├── routes/       # API routes
    │   ├── services/     # Business logic
    │   └── utils/        # Utility functions
    └── config/          # Configuration files
```

## Features
- User Authentication
- Document Management
- AI Chat Interface
- Timeline Tracking
- Resource Center
- Voice Interface

## Tech Stack
- Frontend: React, TailwindCSS, Flowbite
- Backend: Node.js
- Authentication: Social and Email
- AI Integration: Custom AI Agent

## Backend Setup

### Install requirements
pip install -r requirements.txt

### Put all the packages into requirements.txt
pip freeze > requirements.txt

### Run the backend
uvicorn app.main:app --reload

### Check API usage
http://localhost:8000/docs

http://localhost:8000/redocs

### Create tables
scripts/schema.sql

## Frontend Setup

### Install Node.js dependencies
```bash
cd client
npm install
```

### Start the development server
```bash
npm run dev
```
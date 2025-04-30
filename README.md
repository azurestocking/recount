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

| From | Action/Click | To |
|--------------------------|-----------------------------|----------------------------------|
| /login | Login/Signup/Guest | /dashboard |
| /login | Sign Up Now | /signup |
| /dashboard | Action card | /dialogue/text or /dialogue/voice|
| /dashboard | Nav bar | /archive, /resources, /setting |
| /dialogue/text/voice | Nav bar | /dashboard, /archive, etc. |
| /archive | Incident card | /archive/incident/:id |
| /archive/incident/:id | Timeline/Exhibit/Chat card | /archive/incident/:id/timeline, etc. |
| /archive/incident/:id/* | Back arrow | /archive/incident/:id or /archive|
| /resources | Resource link | External URL |
| /setting | Log Out | /login |

## Features
- User Authentication
- Document Management
- AI Chat Interface
- Timeline Tracking
- Resource Center
- Voice Interface

## Development
- Frontend component
- Frontend Scaffold
- Backend Scaffold
- Backend API implementation

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

### Speech Recognition
ffmpeg - https://ffmpeg.org/download.html

Download builds

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
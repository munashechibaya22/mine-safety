# Mine Safety Detection Frontend

React frontend for the mine safety equipment detection system.

## Features

- User authentication (login/register)
- Image and video upload
- Real-time camera capture
- Safety equipment detection results
- Dashboard with analytics
- Detection history

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Build for Production

```bash
npm run build
```

## Technologies

- React 18
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling
- Recharts for data visualization
- Lucide React for icons
- Vite for build tooling

## Project Structure

```
src/
├── api/           # API configuration
├── components/    # Reusable components
├── context/       # React context (Auth)
├── pages/         # Page components
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── Detection.jsx
│   └── History.jsx
├── App.jsx        # Main app component
└── main.jsx       # Entry point
```

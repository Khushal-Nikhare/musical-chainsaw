# Habit Tracker Frontend

A modern React (Vite) frontend for the Habit Tracker application, built with Tailwind CSS, Firebase Authentication, and Axios.

## Prerequisites
- Node.js (v18+)
- Firebase project setup with Google Authentication enabled
- The FastAPI backend running locally or deployed

## Setup Steps

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Environment Variables**
   Create a `.env` file in the root directory and add the following keys from your Firebase Console and backend URL:
   ```env
   VITE_API_URL=http://localhost:8000
   VITE_FIREBASE_API_KEY=your_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_storage_bucket
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
   VITE_FIREBASE_APP_ID=your_app_id
   ```

3. **Run the Development Server**
   ```bash
   npm run dev
   ```

## Tech Stack
- **React + Vite**: Fast, modern frontend framework.
- **Tailwind CSS**: Utility-first CSS framework for styling.
- **Firebase Auth**: Secure Google Sign-In.
- **Axios**: API client configured with auth token interceptors.
- **Recharts**: For displaying 30-day habit history.
- **Lucide React**: Beautiful icons.
- **React Router**: Client-side navigation.

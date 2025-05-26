// Entry point for the frontend app
// TODO: Add app-wide context providers here (e.g., theme, analytics)

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// TODO: Remove this log after verifying API setup
console.log("🌐 VITE_API_URL is:", import.meta.env.VITE_API_URL)

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)

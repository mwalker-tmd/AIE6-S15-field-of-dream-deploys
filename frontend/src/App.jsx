import FileUploader from './components/FileUploader'
import ChatBox from './components/ChatBox'
import { useState } from 'react'
import './App.css' // Layout styles

function App() {
  const [fileUploaded, setFileUploaded] = useState(false)

  return (
    <div className={`app-root ${fileUploaded ? 'chat-mode' : 'initial-mode'}`}>
      <div className="branding">
        {/* TODO: Replace branding logo and app title with your own */}
        <img
          src="/logo_light_transparent.png"
          alt="Your Logo"
          className="logo"
        />
        <h1>AI Agent Chat Template</h1>
      </div>

      {fileUploaded && (
        <div className="chat-section">
          {/* TODO: Customize ChatBox behavior, styling, or replace it entirely */}
          <ChatBox />
        </div>
      )}

      <div className="footer-uploader">
        {/* TODO: Replace FileUploader or bypass if not needed */}
        <FileUploader onUploadSuccess={() => setFileUploaded(true)} />
      </div>
    </div>
  )
}

export default App

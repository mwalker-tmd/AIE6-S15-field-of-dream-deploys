import FileUploader from './components/FileUploader'
import ChatBox from './components/ChatBox'
import { useState } from 'react'
import './App.css' // Layout styles

function App() {
  const [fileUploaded, setFileUploaded] = useState(true)  // Start in chat mode

  const handleNewDocument = () => {
    setFileUploaded(false)
  }

  return (
    <div className="app-root chat-mode">
      <div className="branding">
        <img
          src="/logo_light_transparent.png"
          alt="TMD Open Source RAG Chat"
          className="logo"
        />
        <h1>Open Source RAG Chat</h1>
        <button 
          className="new-document-btn"
          onClick={handleNewDocument}
          title="Upload a new document"
        >
          📄 New Document
        </button>
      </div>

      {fileUploaded ? (
        <div className="chat-section">
          <ChatBox />
        </div>
      ) : (
        <div className="upload-section">
          <FileUploader onUploadSuccess={() => setFileUploaded(true)} />
        </div>
      )}
    </div>
  )
}

export default App

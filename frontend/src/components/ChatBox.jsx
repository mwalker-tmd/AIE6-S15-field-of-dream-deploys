import { useState } from 'react'
import { getApiUrl } from '../utils/env'

export default function ChatBox() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [isStreaming, setIsStreaming] = useState(false)

  const askQuestion = async (e) => {
    e.preventDefault()
    if (!question.trim() || isStreaming) return

    // Add user message to chat history
    const userMessage = { type: 'user', content: question }
    setMessages(prev => [...prev, userMessage])
    
    setIsStreaming(true)
    let aiResponse = ''

    try {
      const formData = new FormData()
      formData.append('question', question)

      const res = await fetch(`${getApiUrl()}/api/ask`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'text/plain',
        },
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.error || `HTTP error! status: ${res.status}`)
      }

      if (res.body) {
        const reader = res.body.getReader()
        const decoder = new TextDecoder('utf-8')
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const text = decoder.decode(value)
          buffer += text

          // Check if we have a complete JSON error message
          try {
            const errorData = JSON.parse(buffer)
            if (errorData.error) {
              throw new Error(errorData.error)
            }
          } catch (e) {
            // Not a JSON error, continue processing as text
            aiResponse += text
            setMessages(prev => {
              const newMessages = [...prev]
              const lastMessage = newMessages[newMessages.length - 1]
              if (lastMessage && lastMessage.type === 'ai') {
                lastMessage.content = aiResponse
                return [...newMessages]
              } else {
                return [...newMessages, { type: 'ai', content: aiResponse }]
              }
            })
            buffer = ''
          }
        }
      } else {
        const data = await res.json()
        aiResponse = data.response || 'No response received'
        setMessages(prev => [...prev, { type: 'ai', content: aiResponse }])
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { type: 'ai', content: 'Error: ' + error.message }])
    } finally {
      setIsStreaming(false)
      setQuestion('')  // Clear the question after sending
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      askQuestion(e)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-messages" data-testid="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">Start a conversation by asking a question...</div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.type === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <div className="message-content">{message.content}</div>
            </div>
          ))
        )}
      </div>

      <div className="question-input-row">
        <textarea
          data-testid="question-input"
          rows={3}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question... (Press Enter to send, Shift+Enter for new line)"
        />

        <button onClick={askQuestion} disabled={isStreaming}>
          {isStreaming ? 'Thinking…' : 'Ask'}
        </button>
      </div>

      <style jsx>{`
        .chat-container {
          display: flex;
          flex-direction: column;
          height: 100%;
          max-width: 800px;
          margin: 0 auto;
          padding: 1rem;
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 1rem;
          display: flex;
          flex-direction: column;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .empty-state {
          text-align: center;
          color: #666;
          padding: 2rem;
        }

        .message {
          max-width: 80%;
          padding: 0.75rem 1rem;
          border-radius: 1rem;
          margin: 0.25rem 0;
        }

        .user-message {
          align-self: flex-end;
          background-color: #007bff;
          color: white;
          border-bottom-right-radius: 0.25rem;
        }

        .ai-message {
          align-self: flex-start;
          background-color: #f0f0f0;
          color: #333;
          border-bottom-left-radius: 0.25rem;
        }

        .message-content {
          white-space: pre-wrap;
          word-break: break-word;
        }

        .question-input-row {
          display: flex;
          gap: 0.5rem;
          padding: 1rem;
          background-color: white;
          border-top: 1px solid #eee;
        }

        textarea {
          flex: 1;
          padding: 0.75rem;
          border: 1px solid #ddd;
          border-radius: 0.5rem;
          resize: none;
          font-family: inherit;
        }

        button {
          padding: 0.75rem 1.5rem;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 0.5rem;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        button:hover:not(:disabled) {
          background-color: #0056b3;
        }

        button:disabled {
          background-color: #ccc;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  )
}

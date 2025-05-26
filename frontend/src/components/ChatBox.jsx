import { useState } from 'react'
import { getApiUrl } from '../utils/env'

export default function ChatBox() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [endpoint, setEndpoint] = useState('/ask')  // or '/agent'

  const askQuestion = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    setIsStreaming(true)
    setResponse('')

    try {
      const formData = new FormData()
      formData.append(endpoint === '/ask' ? 'question' : 'query', question) // flexible

      const res = await fetch(`${getApiUrl()}${endpoint}`, {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        // Try to parse the error response
        try {
          const errorData = await res.json()
          throw new Error(errorData.error || `HTTP error! status: ${res.status}`)
        } catch (e) {
          // If parsing fails, use the status text
          throw new Error(`HTTP error! status: ${res.status}`)
        }
      }

      if (res.body) {
        const reader = res.body.getReader()
        const decoder = new TextDecoder('utf-8')
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          const text = decoder.decode(value)
          try {
            const parsed = JSON.parse(text);
            setResponse(prev => prev + (parsed.response || text));
          } catch {
            setResponse(prev => prev + text);
          }
        }
      } else {
        const data = await res.json()
        setResponse(data.response || 'No response received')
      }
    } catch (error) {
      console.error('Error:', error)
      setResponse('Error: ' + error.message)
    } finally {
      setIsStreaming(false)
    }
  }

  return (
    <>
      {/* TODO: Customize this UI based on your agent or query-based backend */}
      <div className="response-panel" data-testid="response-panel">
        {response || 'Response will appear here...'}
      </div>

      <div className="question-input-row">
        <textarea
          data-testid="question-input"
          rows={3}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
        />

        <select
          value={endpoint}
          onChange={(e) => setEndpoint(e.target.value)}
          disabled={isStreaming}
        >
          <option value="/ask">RAG (/ask)</option>
          <option value="/agent">Agent (/agent)</option>
        </select>

        <button onClick={askQuestion} disabled={isStreaming}>
          {isStreaming ? 'Thinking…' : 'Ask'}
        </button>
      </div>
    </>
  )
}

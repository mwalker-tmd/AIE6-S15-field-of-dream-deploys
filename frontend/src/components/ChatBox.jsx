import { useState } from 'react'
import { getApiUrl } from '../utils/env'

export default function ChatBox() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)

  const askQuestion = async (e) => {
    e.preventDefault()
    if (!question.trim() || isStreaming) return

    setIsStreaming(true)
    setResponse('')

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
            setResponse(prev => prev + text)
            buffer = ''
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
    <>
      <div className="response-panel" data-testid="response-panel">
        {response || 'Response will appear here...'}
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
    </>
  )
}

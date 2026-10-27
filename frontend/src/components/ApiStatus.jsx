import { useEffect, useState } from 'react'
import { getHello } from '../api/client.js'

const LABELS = {
  checking: 'Checking API…',
  connected: 'API connected',
  down: 'API not connected',
}

// shows whether the frontend can reach the flask backend
function ApiStatus() {
  const [status, setStatus] = useState('checking')

  // ask the backend once when the page loads
  useEffect(() => {
    getHello()
      .then(() => setStatus('connected'))
      .catch(() => setStatus('down'))
  }, [])

  return <span className={`api-status ${status}`}>{LABELS[status]}</span>
}

export default ApiStatus

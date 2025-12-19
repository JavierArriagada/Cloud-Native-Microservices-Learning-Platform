import { useState, useEffect } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost/api'

function App() {
  const [apiStatus, setApiStatus] = useState<string>('Checking...')
  const [apiVersion, setApiVersion] = useState<string>('Unknown')

  useEffect(() => {
    // Check API health
    fetch(`${API_URL}/health`)
      .then((res) => res.json())
      .then((data) => {
        setApiStatus(data.status === 'healthy' ? '✅ Healthy' : '❌ Unhealthy')
        setApiVersion(data.version || 'Unknown')
      })
      .catch((error) => {
        console.error('API health check failed:', error)
        setApiStatus('❌ Disconnected')
      })
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚀 Cloud-Native Microservices</h1>
        <p>Learning Platform - React Frontend</p>
      </header>

      <main className="app-main">
        <div className="card">
          <h2>Welcome!</h2>
          <p>This is a React + TypeScript + Vite application.</p>
          <p>Part of the Cloud-Native Microservices Learning Platform.</p>
        </div>

        <div className="card">
          <h3>System Status</h3>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-label">Frontend:</span>
              <span className="status-value">✅ Running</span>
            </div>
            <div className="status-item">
              <span className="status-label">API:</span>
              <span className="status-value">{apiStatus}</span>
            </div>
            <div className="status-item">
              <span className="status-label">API Version:</span>
              <span className="status-value">{apiVersion}</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3>Quick Links</h3>
          <ul className="links-list">
            <li>
              <a href="/api/docs" target="_blank" rel="noopener noreferrer">
                📚 API Documentation (Swagger)
              </a>
            </li>
            <li>
              <a href="/dash" target="_blank" rel="noopener noreferrer">
                📊 Dashboard (Dash)
              </a>
            </li>
            <li>
              <a href="http://localhost:8080" target="_blank" rel="noopener noreferrer">
                🚪 Traefik Dashboard
              </a>
            </li>
            <li>
              <a href="/prometheus" target="_blank" rel="noopener noreferrer">
                📈 Prometheus
              </a>
            </li>
            <li>
              <a href="/grafana" target="_blank" rel="noopener noreferrer">
                📉 Grafana
              </a>
            </li>
            <li>
              <a href="/loki" target="_blank" rel="noopener noreferrer">
                📝 Loki (Logs)
              </a>
            </li>
          </ul>
        </div>

        <div className="card">
          <h3>Next Steps</h3>
          <ol>
            <li>Explore the API documentation</li>
            <li>Check the Dash dashboard</li>
            <li>View metrics in Grafana</li>
            <li>Start building your microservices!</li>
          </ol>
        </div>
      </main>

      <footer className="app-footer">
        <p>Built with React + TypeScript + Vite + FastAPI + Dash + PostgreSQL</p>
        <p>Environment: {import.meta.env.MODE}</p>
      </footer>
    </div>
  )
}

export default App

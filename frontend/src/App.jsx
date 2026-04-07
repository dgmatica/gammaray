import { useEffect, useState } from "react"

// function App() {

function App() {
  const [stats, setStats] = useState(null)
  const [count, setCount] = useState(0)

  useEffect(() => {
    fetch("http://localhost:8000/stats")
      .then(res => res.json())
      .then(data => setStats(data))
  }, [])

  if (!stats) return <p>Loading...</p>

  return (
    <div>
      <h1>Gammaray Dashboard</h1>

      <p>Total requests: {stats.total_requests}</p>
      <ul>
        {Object.entries(stats.statuses).map(([code, count]) => (
          <li key={code}>{code}: {count}</li>
        ))}
      </ul>
      <button onClick={() => setCount(count + 1)}>
        {count}
      </button>
      < Test />
    </div>
  )
}

export default App

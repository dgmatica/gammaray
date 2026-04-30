// src/components/MethodStatusSection.jsx

import { useEffect, useState } from "react"
import { API_BASE_URL } from "../config"

function MethodStatusSection() {
  const [methodStatusData, setMethodStatusData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE_URL}/stats/method-status`)
      .then((response) => {
        if (response.ok === false) {
          throw new Error(`Request failed with status ${response.status}`)
        }

        return response.json()
      })
      .then((data) => {
        setMethodStatusData(data)
      })
      .catch((error) => {
        setError(error.message)
      })
  }, [])

  if (error !== null) {
    return (
      <section className="section">
        <h2 className="section-title">Method Status</h2>
        <p className="section-error">Error: {error}</p>
      </section>
    )
  }

  if (methodStatusData === null) {
    return (
      <section className="section">
        <h2 className="section-title">Method Status</h2>
        <p className="section-placeholder">Loading...</p>
      </section>
    )
  }

  return (
    <section className="section">
      <h2 className="section-title">Method Status</h2>

      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Method</th>
              <th>Status</th>
              <th>Count</th>
              <th>Unique Paths</th>
              <th>Top Paths</th>
            </tr>
          </thead>

          <tbody>
            {methodStatusData.data.map((item) => (
              <tr key={`${item.method}-${item.status}`}>
                <td>{item.method}</td>
                <td>{item.status}</td>
                <td>{item.count}</td>
                <td>{item.unique_paths_count}</td>
                <td>
                  <ul className="compact-list">
                    {item.top_paths.map((pathItem) => (
                      <li key={pathItem.path}>
                        <span className="path-text">{pathItem.path}</span>
                        <span className="muted-count"> × {pathItem.count}</span>
                      </li>
                    ))}
                  </ul>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default MethodStatusSection

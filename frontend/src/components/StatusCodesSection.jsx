import { useEffect, useState } from "react"
import { API_BASE_URL } from "../config"

function StatusCodesSection() {
  const [statusCodesData, setStatusCodesData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE_URL}/stats/status-codes`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load status codes")
        }

        return response.json()
      })
      .then((data) => {
        setStatusCodesData(data)
        setError(null)
      })
      .catch(() => {
        setError("Could not load status codes")
      })
  }, [])

  let statusCodeRows = []

  if (statusCodesData && statusCodesData.data) {
    statusCodeRows = Object.entries(statusCodesData.data)

    statusCodeRows.sort((leftEntry, rightEntry) => {
      const leftCount = leftEntry[1]
      const rightCount = rightEntry[1]

      return rightCount - leftCount
    })
  }

  return (
    <section className="section">
      <h2 className="section-title">Status Codes</h2>

      {error ? (
        <p className="section-placeholder">{error}</p>
      ) : !statusCodesData ? (
        <p className="section-placeholder">Loading status codes...</p>
      ) : (
        <div className="table-wrap">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Status</th>
                <th>Count</th>
              </tr>
            </thead>

            <tbody>
              {statusCodeRows.map((entry) => {
                const statusCode = entry[0]
                const count = entry[1]

                return (
                  <tr key={statusCode}>
                    <td>{statusCode}</td>
                    <td>{count}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default StatusCodesSection

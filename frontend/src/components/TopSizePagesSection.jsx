import { useEffect, useState } from "react"
import { API_BASE_URL } from "../config"

function formatBytes(bytes) {
  if (bytes === 0) {
    return "0 B"
  }

  if (bytes < 1024) {
    return `${bytes.toFixed(0)} B`
  }

  const kilobytes = bytes / 1024

  if (kilobytes < 1024) {
    return `${kilobytes.toFixed(2)} KB`
  }

  const megabytes = kilobytes / 1024

  return `${megabytes.toFixed(2)} MB`
}

function TopSizePagesSection() {
  const [topSizePagesData, setTopSizePagesData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE_URL}/stats/top-size-pages`)
      .then((response) => {
        if (response.ok === false) {
          throw new Error(`Request failed with status ${response.status}`)
        }

        return response.json()
      })
      .then((data) => {
        setTopSizePagesData(data)
      })
      .catch((error) => {
        setError(error.message)
      })
  }, [])

  if (error !== null) {
    return (
      <section className="section">
        <h2 className="section-title">Top Size Pages</h2>
        <p className="section-error">Error: {error}</p>
      </section>
    )
  }

  if (topSizePagesData === null) {
    return (
      <section className="section">
        <h2 className="section-title">Top Size Pages</h2>
        <p className="section-placeholder">Loading...</p>
      </section>
    )
  }

  return (
    <section className="section">
      <h2 className="section-title">Top Size Pages</h2>

      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Path</th>
              <th>Avg Size</th>
              <th>Total Size</th>
              <th>Count</th>
            </tr>
          </thead>

          <tbody>
            {topSizePagesData.data.map((page, index) => (
              <tr key={page.path}>
                <td>{index + 1}</td>
                <td>{page.path}</td>
                <td>{formatBytes(page.avg_size)}</td>
                <td>{formatBytes(page.total_size)}</td>
                <td>{page.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default TopSizePagesSection

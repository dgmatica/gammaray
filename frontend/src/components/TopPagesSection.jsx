import { useEffect, useState } from "react"
import { API_BASE_URL } from "../config"

function TopPagesSection() {
  const [topPagesData, setTopPagesData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE_URL}/stats/top-pages`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load top pages")
        }

        return res.json()
      })
      .then((data) => {
        setTopPagesData(data)
        setError(null)
      })
      .catch(() => {
        setError("Could not load top pages")
      })
  }, [])

  return (
    <section className="section section-top-pages">
      <h2 className="section-title">Top Pages</h2>

      {error ? (
        <p className="section-placeholder">{error}</p>
      ) : !topPagesData ? (
        <p className="section-placeholder">Loading top pages...</p>
      ) : (
        <div className="table-wrap">
          <table className="stats-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Path</th>
                <th>Count</th>
              </tr>
            </thead>

            <tbody>
              {topPagesData.data.map((page, index) => (
                <tr key={page.path}>
                  <td>{index + 1}</td>
                  <td>{page.path}</td>
                  <td>{page.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default TopPagesSection

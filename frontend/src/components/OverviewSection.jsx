import { useEffect, useState } from "react"
import OverviewCard from "./OverviewCard"
import OverviewSkeleton from "./OverviewSkeleton"

function OverviewSection() {
  const [overview, setOverview] = useState(null)

  useEffect(() => {
    fetch("http://localhost:8000/stats/overview")
      .then((res) => res.json())
      .then((data) => setOverview(data))
  }, [])

  if (!overview) {
    return <OverviewSkeleton />
  }

  const topStatusValue = overview.top_status_code
    ? `${overview.top_status_code.status} (${overview.top_status_code.count})`
    : "No data"

  const topPageValue = overview.top_page
    ? `${overview.top_page.path} (${overview.top_page.count})`
    : "No data"

  const topMethodStatusValue = overview.top_method_status
    ? `${overview.top_method_status.method} ${overview.top_method_status.status} (${overview.top_method_status.count})`
    : "No data"

  const avgDurationValue =
    overview.avg_duration !== null
      ? overview.avg_duration.toFixed(3)
      : "No data"

  const avgSizeValue =
    overview.avg_size !== null
      ? overview.avg_size.toFixed(3)
      : "No data"

  return (
    <section className="section overview">
      <h2 className="section-title">Overview</h2>

      <div className="overview-grid">
        <OverviewCard
          label="Valid logs"
          value={overview.total_valid_logs}
        />

        <OverviewCard
          label="Failed logs"
          value={overview.total_failed_logs}
        />

        <OverviewCard
          label="Unique paths"
          value={overview.unique_paths}
        />

        <OverviewCard
          label="Top status"
          value={topStatusValue}
        />

        <OverviewCard
          label="Top page"
          value={topPageValue}
        />

        <OverviewCard
          label="Top method/status"
          value={topMethodStatusValue}
        />

        <OverviewCard
          label="Avg duration"
          value={avgDurationValue}
        />

        <OverviewCard
          label="Avg size"
          value={avgSizeValue}
        />
      </div>
    </section>
  )
}

export default OverviewSection

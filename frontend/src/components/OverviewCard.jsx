function OverviewCard({ label, value }) {
  return (
    <div className="overview-card">
      <span className="overview-label">{label}</span>
      <span className="overview-value">{value}</span>
    </div>
  )
}

export default OverviewCard

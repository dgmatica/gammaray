import "./App.css"
import OverviewSection from "./components/OverviewSection"

function App() {
  return (
    <div className="app">
      <h1 className="page-title">SYNTHROPY DASHBOARD</h1>

      <OverviewSection />

      <section className="section">
        <h2 className="section-title section-top-pages">Top Pages</h2>
        <p>Placeholder</p>
      </section>

      <section className="section">
        <h2 className="section-title section-status-codes">Status Codes</h2>
        <p>Placeholder</p>
      </section>

      <section className="section">
        <h2 className="section-title section-top-sizes">Top Size Pages</h2>
        <p>Placeholder</p>
      </section>

      <section className="section">
        <h2 className="section-title section-method-status">Method Status</h2>
        <p>Placeholder</p>
      </section>
    </div>
  )
}

export default App

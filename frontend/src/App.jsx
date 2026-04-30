import "./App.css"
import OverviewSection from "./components/OverviewSection"
import TopPagesSection from "./components/TopPagesSection"
import StatusCodesSection from "./components/StatusCodesSection"
import TopSizePagesSection from "./components/TopSizePagesSection"
import MethodStatusSection from "./components/MethodStatusSection"


function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1 className="page-title">SYNTHROPY DASHBOARD</h1>
      </header>

      <main className="dashboard-grid">
        <div className="panel panel-overview">
          <OverviewSection />
        </div>

        <div className="panel panel-top-pages">
          <TopPagesSection />
        </div>

        <div className="panel panel-status-codes">
          <StatusCodesSection />
        </div>

        <div className="panel panel-top-size">
          <TopSizePagesSection />
        </div>

        <div className="panel panel-method-status">
          <MethodStatusSection />
        </div>
      </main>
    </div>
  )
}

export default App

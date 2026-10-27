import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import CampaignsPage from './pages/CampaignsPage.jsx'
import SitesPage from './pages/SitesPage.jsx'
import MapPage from './pages/MapPage.jsx'
import ResultsPage from './pages/ResultsPage.jsx'
import ApiStatus from './components/ApiStatus.jsx'

function App() {
  return (
    <>
      <header>
        <h1>Mobile Vaccination Planner</h1>
        <nav>
          <NavLink to="/campaigns">Campaigns</NavLink>
          <NavLink to="/sites">Sites</NavLink>
          <NavLink to="/map">Map</NavLink>
          <NavLink to="/results">Results</NavLink>
        </nav>
        <ApiStatus />
      </header>
      <main>
        <Routes>
          {/* start on the campaigns page */}
          <Route path="/" element={<Navigate to="/campaigns" replace />} />
          <Route path="/campaigns" element={<CampaignsPage />} />
          <Route path="/sites" element={<SitesPage />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </main>
    </>
  )
}

export default App

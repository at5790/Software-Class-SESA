import { useState } from 'react'
import AddSiteForm from '../components/AddSiteForm.jsx'
import SitesTable from '../components/SitesTable.jsx'
import mockSites from '../data/mockSites.js'

// lists the vaccination sites, using mock data for now
function SitesPage() {
  const [sites, setSites] = useState(mockSites)

  // new sites start active, and get a temporary id until the backend gives one
  function addSite(site) {
    setSites([...sites, { ...site, id: String(Date.now()), active: true }])
  }

  return (
    <section>
      <h2>Sites</h2>
      <AddSiteForm onAdd={addSite} />
      <SitesTable sites={sites} />
    </section>
  )
}

export default SitesPage

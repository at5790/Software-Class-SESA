import { useState } from 'react'
import SitesTable from '../components/SitesTable.jsx'
import mockSites from '../data/mockSites.js'

// lists the vaccination sites, using mock data for now
function SitesPage() {
  // kept in state so the add form can change it later
  const [sites] = useState(mockSites)

  return (
    <section>
      <h2>Sites</h2>
      <SitesTable sites={sites} />
    </section>
  )
}

export default SitesPage

import mockSites from '../data/mockSites.js'

// lists the vaccination sites, using mock data for now
function SitesPage() {
  return (
    <section>
      <h2>Sites</h2>
      <ul>
        {mockSites.map((site) => (
          <li key={site.id}>{site.name}</li>
        ))}
      </ul>
    </section>
  )
}

export default SitesPage

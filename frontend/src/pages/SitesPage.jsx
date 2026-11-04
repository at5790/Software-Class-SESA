import mockSites from '../data/mockSites.js'

// lists the vaccination sites, using mock data for now
function SitesPage() {
  return (
    <section>
      <h2>Sites</h2>
      <table className="sites-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Capacity</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {mockSites.map((site) => (
            <tr key={site.id}>
              <td>{site.name}</td>
              <td>{site.address}</td>
              <td>{site.capacity}</td>
              <td>{site.active ? 'Active' : 'Inactive'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}

export default SitesPage

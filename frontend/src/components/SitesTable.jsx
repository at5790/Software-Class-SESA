// table of sites, shows whatever list it's given
function SitesTable({ sites }) {
  return (
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
        {sites.map((site) => (
          <tr key={site.id}>
            <td>{site.name}</td>
            <td>{site.address}</td>
            <td>{site.capacity}</td>
            <td>{site.active ? 'Active' : 'Inactive'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default SitesTable

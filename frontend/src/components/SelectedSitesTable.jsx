// table of the sites the optimizer picked
function SelectedSitesTable({ sites }) {
  if (sites.length === 0) {
    return <p>No sites selected</p>
  }

  return (
    <table className="sites-table">
      <thead>
        <tr>
          <th>Site</th>
          <th>People reached</th>
          <th>Doses</th>
          <th>Areas covered</th>
        </tr>
      </thead>
      <tbody>
        {sites.map((site) => (
          <tr key={site.site_id}>
            <td>{site.site_id}</td>
            <td>{site.gain.toLocaleString('en-US')}</td>
            <td>{site.doses.toLocaleString('en-US')}</td>
            <td>{site.new_area_ids.length}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default SelectedSitesTable

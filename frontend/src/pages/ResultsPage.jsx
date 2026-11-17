import mockResult from '../data/mockResult.js'

// shows what the optimizer picked, using a mock result for now
function ResultsPage() {
  const { metrics } = mockResult
  const stats = [
    ['Coverage before', `${metrics.baseline_coverage_pct}%`],
    ['Coverage after', `${metrics.post_coverage_pct}%`],
    ['People newly reached', metrics.additional_population.toLocaleString('en-US')],
    ['Sites selected', metrics.sites_selected],
    ['Doses allocated', metrics.doses_allocated.toLocaleString('en-US')],
    ['Doses unused', metrics.doses_unused.toLocaleString('en-US')],
  ]

  return (
    <section>
      <h2>Results</h2>
      <div className="result-stats">
        {stats.map(([label, value]) => (
          <div className="stat" key={label}>
            <span className="stat-value">{value}</span>
            <span className="stat-label">{label}</span>
          </div>
        ))}
      </div>
    </section>
  )
}

export default ResultsPage

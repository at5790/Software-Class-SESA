import { useState } from 'react'

// field names match campaign_model in server/endpoints.py
export const LABELS = {
  available_doses: 'Available doses',
  mobile_units: 'Mobile units',
  max_sites: 'Max sites',
  radius: 'Radius (km)',
  objective: 'Objective',
}

export const NUMBER_FIELDS = ['available_doses', 'mobile_units', 'max_sites', 'radius']

// only one optimizer for now
export const OBJECTIVES = { max_coverage: 'Maximum coverage' }

const EMPTY = {
  available_doses: '',
  mobile_units: '',
  max_sites: '',
  radius: '',
  objective: 'max_coverage',
}

// form for the campaign limits, passes the campaign to onSubmit
function CampaignForm({ onSubmit }) {
  const [form, setForm] = useState(EMPTY)

  // one handler for every field, uses the input's name
  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  function handleSubmit(event) {
    event.preventDefault()
    const campaign = { objective: form.objective }
    for (const name of NUMBER_FIELDS) {
      campaign[name] = Number(form[name])
    }
    onSubmit(campaign)
  }

  return (
    <form className="campaign-form" onSubmit={handleSubmit}>
      {NUMBER_FIELDS.map((name) => (
        <label key={name}>
          {LABELS[name]}
          <input type="number" step="any" name={name} value={form[name]} onChange={handleChange} />
        </label>
      ))}
      <label>
        {LABELS.objective}
        <select name="objective" value={form.objective} onChange={handleChange}>
          {Object.entries(OBJECTIVES).map(([value, text]) => (
            <option key={value} value={value}>{text}</option>
          ))}
        </select>
      </label>
      <button type="submit">Create campaign</button>
    </form>
  )
}

export default CampaignForm

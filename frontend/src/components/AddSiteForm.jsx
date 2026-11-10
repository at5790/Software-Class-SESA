import { useState } from 'react'

// form for adding a new site, passes it to onAdd
function AddSiteForm({ onAdd }) {
  const [name, setName] = useState('')
  const [address, setAddress] = useState('')
  const [capacity, setCapacity] = useState('')

  function handleSubmit(event) {
    // stop the browser from reloading the page
    event.preventDefault()
    onAdd({ name, address, capacity: Number(capacity) })
    setName('')
    setAddress('')
    setCapacity('')
  }

  return (
    <form className="add-site-form" onSubmit={handleSubmit}>
      <label>
        Name
        <input value={name} onChange={(e) => setName(e.target.value)} />
      </label>
      <label>
        Address
        <input value={address} onChange={(e) => setAddress(e.target.value)} />
      </label>
      <label>
        Capacity
        <input type="number" value={capacity} onChange={(e) => setCapacity(e.target.value)} />
      </label>
      <button type="submit">Add site</button>
    </form>
  )
}

export default AddSiteForm

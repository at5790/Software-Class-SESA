import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test, vi } from 'vitest'
import AddSiteForm from './AddSiteForm.jsx'

// fill in every field and click add
async function fillAndSubmit(user) {
  await user.type(screen.getByLabelText('Name'), 'New Clinic')
  await user.type(screen.getByLabelText('Address'), '5 New St')
  await user.type(screen.getByLabelText('Capacity'), '80')
  await user.click(screen.getByRole('button', { name: 'Add site' }))
}

test('passes the typed site to onAdd', async () => {
  const user = userEvent.setup()
  const onAdd = vi.fn()
  render(<AddSiteForm onAdd={onAdd} />)
  await fillAndSubmit(user)
  expect(onAdd).toHaveBeenCalledWith({ name: 'New Clinic', address: '5 New St', capacity: 80 })
})

test('clears the fields after adding', async () => {
  const user = userEvent.setup()
  render(<AddSiteForm onAdd={vi.fn()} />)
  await fillAndSubmit(user)
  expect(screen.getByLabelText('Name').value).toBe('')
  expect(screen.getByLabelText('Address').value).toBe('')
  expect(screen.getByLabelText('Capacity').value).toBe('')
})

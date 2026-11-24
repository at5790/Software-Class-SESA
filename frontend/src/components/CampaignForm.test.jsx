import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test, vi } from 'vitest'
import CampaignForm, { LABELS, OBJECTIVES } from './CampaignForm.jsx'

test('passes the entered campaign to onSubmit as numbers', async () => {
  const user = userEvent.setup()
  const onSubmit = vi.fn()
  render(<CampaignForm onSubmit={onSubmit} />)
  await user.type(screen.getByLabelText(LABELS.available_doses), '1000')
  await user.type(screen.getByLabelText(LABELS.mobile_units), '3')
  await user.type(screen.getByLabelText(LABELS.max_sites), '5')
  await user.type(screen.getByLabelText(LABELS.radius), '2.5')
  await user.click(screen.getByRole('button'))
  expect(onSubmit).toHaveBeenCalledWith({
    available_doses: 1000,
    mobile_units: 3,
    max_sites: 5,
    radius: 2.5,
    objective: 'max_coverage',
  })
})

test('starts with maximum coverage as the objective', () => {
  render(<CampaignForm onSubmit={vi.fn()} />)
  const select = screen.getByLabelText(LABELS.objective)
  expect(select.value).toBe('max_coverage')
  expect(screen.getByRole('option', { name: OBJECTIVES.max_coverage })).toBeTruthy()
})

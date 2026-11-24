import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test } from 'vitest'
import { LABELS } from '../components/CampaignForm.jsx'
import CampaignsPage, { READY_TITLE } from './CampaignsPage.jsx'

test('shows no summary before a campaign is created', () => {
  render(<CampaignsPage />)
  expect(screen.queryByText(READY_TITLE)).toBeNull()
})

test('shows a summary after creating a campaign', async () => {
  const user = userEvent.setup()
  render(<CampaignsPage />)
  await user.type(screen.getByLabelText(LABELS.available_doses), '1000')
  await user.type(screen.getByLabelText(LABELS.radius), '2.5')
  await user.click(screen.getByRole('button'))
  expect(screen.getByText(READY_TITLE)).toBeTruthy()
  expect(screen.getByText(`${LABELS.available_doses}: 1000`)).toBeTruthy()
  expect(screen.getByText(`${LABELS.radius}: 2.5`)).toBeTruthy()
})

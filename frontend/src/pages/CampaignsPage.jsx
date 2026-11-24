import { useState } from 'react'
import CampaignForm, { LABELS, OBJECTIVES } from '../components/CampaignForm.jsx'

export const READY_TITLE = 'Campaign ready'

// enter the campaign limits, shows what was entered for now
function CampaignsPage() {
  const [campaign, setCampaign] = useState(null)

  return (
    <section>
      <h2>Campaigns</h2>
      <CampaignForm onSubmit={setCampaign} />
      {campaign && (
        <div className="campaign-summary">
          <h3>{READY_TITLE}</h3>
          <ul>
            <li>{`${LABELS.available_doses}: ${campaign.available_doses}`}</li>
            <li>{`${LABELS.mobile_units}: ${campaign.mobile_units}`}</li>
            <li>{`${LABELS.max_sites}: ${campaign.max_sites}`}</li>
            <li>{`${LABELS.radius}: ${campaign.radius}`}</li>
            <li>{`${LABELS.objective}: ${OBJECTIVES[campaign.objective]}`}</li>
          </ul>
        </div>
      )}
    </section>
  )
}

export default CampaignsPage

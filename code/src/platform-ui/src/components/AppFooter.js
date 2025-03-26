import React from 'react'
import { CFooter } from '@coreui/react'

const AppFooter = () => {
  return (
    <CFooter className="px-4">
      <div>
        <a href="" rel="noopener noreferrer">
          Core Team
        </a>
        <span className="ms-1">&copy; 2025</span>
      </div>
      <div className="ms-auto">
        <span className="me-1">Powered by</span>
        <a href="" rel="noopener noreferrer">
          Mind Over Machines
        </a>
      </div>
    </CFooter>
  )
}

export default React.memo(AppFooter)

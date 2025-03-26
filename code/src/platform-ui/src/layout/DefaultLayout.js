import React from 'react'
import { AppContent, AppSidebar, AppFooter, AppHeader } from '../components/index'
import ChatbotComponent from '../views/bot/chatbot'

const DefaultLayout = () => {
  return (
    <div>
      <AppSidebar />
      <div className="wrapper d-flex flex-column min-vh-100">
        <AppHeader />
        <div className="body flex-grow-1">
          <AppContent />
        </div>
        <div style={{ position: 'relative', zIndex: 100 }}>
          <ChatbotComponent />
        </div>
        <AppFooter />
      </div>
    </div>
  )
}

export default DefaultLayout

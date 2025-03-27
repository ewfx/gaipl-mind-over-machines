/* eslint-disable prettier/prettier */
// components/Sidebar.js
import React from 'react'
import DraggableComponent from './DraggableComponent'

const Sidebar = () => {
  const components = [
    { name: 'Metrics' },
    { name: 'Incidents' },
    { name: 'KB' },
  ]

  return (
    <div
      style={{
        width: '30%',
        padding: '100px',
        background: '#f4f4f4',
        maxHeight: '60vh',
        borderRight: '2px solid #ddd',
      }}
    >
      <h5 style={{ textAlign: 'center', marginBottom: '15px', marginLeft: '-55px' }}>Agentic Tools</h5>
      {components.map((comp, index) => (
        <DraggableComponent key={index} {...comp} />
      ))}
    </div>
  )
}

export default Sidebar

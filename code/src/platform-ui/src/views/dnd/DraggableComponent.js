/* eslint-disable prettier/prettier */
// components/DraggableComponent.js
import React from 'react'
import { useDrag } from 'react-dnd'

const DraggableComponent = ({ name, image, description }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'COMPONENT',
    item: { name, image, description },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }))

  return (
    <div
      style={{
        display: "flex", // Align items in a row
        gap: "15px", // Space between components
        flexWrap: "wrap", // Wrap items to next line if needed
        justifyContent: "center", // Center items
        padding: "20px",
        float: "left",
      }}
    >
      <div
        ref={drag}
        style={{
          width: "80px",
          height: "80px",
          float: "left",
          padding: "15px",
          background: isDragging
            ? "linear-gradient(145deg, #d1e7fd, #c2d9fa)"
            : "linear-gradient(145deg, #ffffff, #e6e6e6)",
          borderRadius: "50%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          boxShadow: isDragging
            ? "inset 2px 2px 5px rgba(0,0,0,0.2), inset -2px -2px 5px rgba(255,255,255,0.8)"
            : "5px 5px 10px rgba(0,0,0,0.3), -5px -5px 10px rgba(255,255,255,0.8)",
          cursor: "grab",
          transition: "transform 0.2s ease-in-out",
        }}
        onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.05)")}
        onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
      >
        {image && (
          <img
            src={image}
            alt={name}
            style={{
              width: "50px",
              height: "50px",
              marginBottom: "5px",
              borderRadius: "50%",
            }}
          />
        )}
        <strong style={{ fontSize: "14px", color: "#333" }}>{name}</strong>
        {description && (
          <p
            style={{
              fontSize: "10px",
              color: "#666",
              textAlign: "center",
              padding: "0 5px",
            }}
          >
            {description}
          </p>
        )}
      </div>
    </div>
  );
  
  
}

export default DraggableComponent

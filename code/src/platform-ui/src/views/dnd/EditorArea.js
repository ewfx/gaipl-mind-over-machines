/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from "react";
import { useDrop } from "react-dnd";
import ApiService from '../../apiService';

const DropArea = () => {
  const [droppedItems, setDroppedItems] = useState([]);

  // Handle drop event
  const [, drop] = useDrop(() => ({
    accept: "COMPONENT",
    drop: (item) => {
      setDroppedItems((prevItems) => {
        const updatedItems = prevItems.some((i) => i.name === item.name)
          ? prevItems // Prevent duplicate drops
          : [...prevItems, item];

        return updatedItems;
      });
    },
  }));

  // Function to construct and send API request when droppedItems change
  useEffect(() => {
    if (droppedItems.length === 0) return;

    const updateIncidentMessage = (tools) => {
      const toolsList = tools.map((item) => item.name).join(", ");
      const message =
        tools.length > 0
          ? `Welcome to the Lang Page! 🚀 Currently active tools: ${toolsList}. Let me know if you need assistance! 😊`
          : `Welcome to the Lang Page! 🚀 Let me know if you need assistance! 😊`;

      const userData = {
        message,
        page: "tools",
        id: "1",
        dataId: "1234",
        tools: tools.map((item) => item.name),
      };

      ApiService.postIncident(userData);
    };

    updateIncidentMessage(droppedItems);
  }, [droppedItems]); // Runs every time droppedItems changes

  // Function to remove an item from the list
  const removeItem = (index) => {
    setDroppedItems((prevItems) => prevItems.filter((_, i) => i !== index));
  };

  return (
    <div
      ref={drop}
      style={{
        width: "60%",
        padding: "20px",
        maxHeight: "60vh",
        background: "rgb(232 232 186)",
        display: "flex",
        flexWrap: "wrap",
        gap: "20px",
        justifyContent: "center",
        alignItems: "center",
        position: "relative",
        border: "2px dashed #bbb",
      }}
    >
      <h3 style={{ position: "absolute", top: "10px", color: "#555" }}>
        Drop the tools - create Langchain
      </h3>
  
      {droppedItems.map((item, index) => (
        <div
          key={index}
          style={{
            width: "120px",
            height: "120px",
            background: "linear-gradient(145deg, #ffffff, #e6e6e6)",
            borderRadius: "50%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "5px 5px 10px rgba(0,0,0,0.3), -5px -5px 10px rgba(255,255,255,0.8)",
            position: "relative",
            transform: "rotate(-3deg)",
            transition: "transform 0.2s ease-in-out",
          }}
          onMouseEnter={(e) => (e.currentTarget.style.transform = "rotate(0deg) scale(1.05)")}
          onMouseLeave={(e) => (e.currentTarget.style.transform = "rotate(-3deg) scale(1)")}
        >
          {item.image && (
            <img
              src={item.image}
              alt={item.name}
              style={{ width: "40px", height: "40px", marginBottom: "5px", borderRadius: "50%" }}
            />
          )}
          <strong style={{ fontSize: "14px", color: "#333" }}>{item.name}</strong>
  
          {item.description && (
            <p style={{ fontSize: "10px", color: "#666", textAlign: "center", padding: "0 5px" }}>
              {item.description}
            </p>
          )}
  
          {/* Featuristic Close Button (Sticky Pin Look) */}
          <button
            onClick={() => removeItem(index)}
            style={{
              position: "absolute",
              top: "-8px",
              right: "-8px",
              background: "radial-gradient(circle, red 40%, darkred 80%)",
              color: "white",
              border: "2px solid white",
              borderRadius: "50%",
              width: "24px",
              height: "24px",
              cursor: "pointer",
              fontSize: "14px",
              fontWeight: "bold",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "2px 2px 5px rgba(0,0,0,0.4)",
              transition: "transform 0.2s ease-in-out",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.2)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
          >
            ✖
          </button>
        </div>
      ))}
    </div>
  );
  
};

export default DropArea;

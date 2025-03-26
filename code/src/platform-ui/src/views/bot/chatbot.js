/* eslint-disable prettier/prettier */
// src/components/Chatbot.js
import React, { useState, useRef, useEffect } from "react";

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false); // State to track chatbot visibility
  const iframeRef = useRef(null);

  const sendMessageToIframe = (message) => {
    console.log(message);
    const iframe = document.getElementById("chainlit-iframe");
    console.log(iframe);
    if (iframe) {
      console.log("📤 Sending message to iframe:", message);
      iframe.contentWindow.postMessage({ type: "NEW_MESSAGE", content: message }, "*");
    }
    const sendMessage = () => {
      iframe.contentWindow.postMessage({ text: "Hi welcome" }, "*");
    };

    if (iframe) {
      iframe.addEventListener("load", sendMessage);
    }

    return () => {
      if (iframe) {
        iframe.removeEventListener("load", sendMessage);
      }
    };
  };

  const openChatbot = (status) => {
    setIsOpen(status); // Show iframe
    
    setTimeout(() => {
      if (iframeRef.current && iframeRef.current.contentWindow) {
        const message = {
          type: "PAGE_DETAILS",
          url: window.location.href,
          title: document.title,
          userId: "user_123", // Example user ID
        };
        console.log("📤 Sending message to iframe:", message);
        iframeRef.current.contentWindow.postMessage(message, "http://localhost:9002");
        sendMessageToIframe("Hiiiiiiiiiiii");
      }
    }, 2000); // Delay to ensure iframe is fully loaded
    
  };

  // Listen for messages from the iframe
  useEffect(() => {
    const handleMessage = (event) => {
      console.log("🔥 Message received from Chainlit:", event.data);
    };

    window.addEventListener("message", handleMessage);
    return () => {
      window.removeEventListener("message", handleMessage);
    };
  }, []);

  return (
    <div>
      {/* Chat Icon */}
      <div
        style={{
          position: "fixed",
          bottom: "50px",
          right: "50px",
          width: "80px",
          height: "80px",
          backgroundColor: "#007bff",
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          zIndex: 1000,
          boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
          transition: "transform 0.3s ease-in-out", // Smooth hover effect
        }}
        onClick={() => openChatbot(!isOpen)} // Toggle chatbot visibility on click
      >
        <span style={{ color: "#fff", fontSize: "48px" }}>💬</span> {/* Chat icon */}
      </div>

      {/* iFrame Container */}
      {isOpen && (
        <div
          style={{
            position: "fixed",
            bottom: "120px", // Adjusted to account for the chat icon
            right: "100px",
            width: "600px", // Width of the iframe
            height: "600px", // Height of the iframe
            border: "1px solid #ccc",
            borderRadius: "10px",
            overflow: "hidden", // Ensure no overflow
            zIndex: 1000,
            transform: isOpen ? "scale(1) rotateX(0deg)" : "scale(0) rotateX(-20deg)", // 3D rotation
            transition: "transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out", // Smooth transitions
            transformOrigin: "bottom right", // Animate from the bottom-right corner
            boxShadow: isOpen
              ? "0px 10px 20px rgba(0, 0, 0, 0.2), 0px 6px 6px rgba(0, 0, 0, 0.1)" // Shadow when open
              : "0px 4px 6px rgba(0, 0, 0, 0.1)", // Shadow when closed
          }}
        >
          {/* iFrame */}
          <iframe
            id="chainlit-iframe"
            ref={iframeRef}
            src="http://localhost:9002" // Replace with your Chainlit app URL
            title="Embedded App"
            style={{
              width: "100%",
              height: "100%",
              border: "none",
            }}
          />
        </div>
      )}
    </div>
  );
};

export default Chatbot;

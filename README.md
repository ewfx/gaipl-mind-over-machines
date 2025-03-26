# 🚀 Gen-AI Enabled Integrated Platform Environment

Develop a **Gen-AI enabled Integrated Platform Environment** that provides an integrated console to our platform support teams, empowering them with various capabilities such as incident resolution, AI-based root cause analysis, automated workflows, and more.

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This project aims to revolutionize platform support by creating an **AI-powered integrated platform environment**. Our solution leverages **Llama70B** AI models, **Chainlit** for real-time conversational interfaces, and **OpenShift** for scalable deployment, ensuring that platform support teams can efficiently resolve incidents and improve system health through automation and real-time insights.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
The inspiration behind this project came from the need to automate incident management and improve platform performance monitoring. By combining **AI-powered insights** with **real-time monitoring**, we aim to assist support teams in identifying, diagnosing, and resolving issues faster and more effectively.

## ⚙️ What It Does
- **Incident Resolution**: Automatically generate and resolve incidents, reducing manual intervention.
- **AI Chatbot Assistance**: Provide context-based incident resolution and root cause analysis through an AI-driven chatbot.
- **Real-Time Monitoring**: Track system health, CPU, memory usage, and more, with the ability to scale based on load.
- **ServiceNow Integration**: Seamlessly integrate with ServiceNow for automatic ticket creation and updates.
- **ElasticSearch Integration**: Leverage ElasticSearch for indexing and searching incident-related data.

## 🛠️ How We Built It
We built the **Gen-AI enabled Integrated Platform Environment** using the following technologies:
- **Frontend**: Built using **React** for an intuitive and responsive user interface.
- **Backend**: Powered by **Python**, providing robust APIs and incident handling logic.
- **Database**: **ElasticSearch** for fast and scalable indexing of incident data.
- **AI Chatbot**: Integrated with **Chainlit** and **Llama70B** for real-time, contextual assistance.
- **Deployment**: Deployed on **OpenShift** to ensure scalability and availability.
- **Incident Management**: Integrated with **ServiceNow** to automate ticket generation and status updates.

## 🚧 Challenges We Faced
- **Integration Complexity**: Integrating multiple tools like **OpenShift**, **ElasticSearch**, **ServiceNow**, and **AI models** was a complex task requiring seamless communication between components.
- **Real-Time Performance**: Ensuring that the AI-driven chatbot could handle real-time queries without latency was challenging, especially with large-scale incidents.
- **Scaling Issues**: Properly scaling the platform to handle multiple concurrent incidents required efficient load balancing and resource management with OpenShift.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone [https://github.com/your-repo/genal-platform.git](https://github.com/ewfx/gaipl-mind-over-machines.git)

### Install dependencies

1. Python backend:  
   ```sh
   pip install -r requirements.txt

# Project Setup Guide

## Set Up Docker and ElasticSearch

### Ensure Docker is Installed and Running

Make sure that **Docker** is installed on your machine and running properly. You can download Docker from [here](https://www.docker.com/products/docker-desktop).

### ElasticSearch Configuration

Follow the official ElasticSearch setup guides to configure the environment for real-time indexing:

- [ElasticSearch Installation Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)

Ensure that **ElasticSearch** is properly set up in Docker.

---

## Running the Project

### 1. Start the React Frontend:

To start the React frontend, run the following command:

```sh
npm start



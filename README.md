# Overview

Chapiana is a fully functional real time chat application designed for seamless and instant messaging. Built with a scalable backend architecture and an intuitive frontend interface, this application supports one-on-one messaging, group chats, and live status updates. 

The system ensures efficient message delivery using WebSockets, providing a smooth real time communication experience.

## Key Features
- Instant Messaging

  Real-time chat functionality with WebSockets for minimal latency.

- User Authentication
  
  Secure login and registration system with JWT-based authentication.
  
- One-on-One & Group Chats

  Private conversations and group discussions with dynamic user management.

- Typing Indicators & Read Receipts

  Real time feedback on message interactions.

- Notifications

  Instant alerts for new messages and mentions.

- Message History & Persistence

  Stored chat history for seamless access across sessions.

- Scalability

 Optimized for high performance and scalable deployments.

## Tech Stack
- Backend

  Python (Django, Django Channels), Redis, PostgreSQL

- Frontend: Vue.js / React (Choose based on your implementation)

- WebSockets

  Django Channels for real time communication

- Authentication

  JWT for secure user sessions

- Database

  PostgreSQL for storing user and chat data

- Deployment

  Docker, Nginx, and Gunicorn for production readiness


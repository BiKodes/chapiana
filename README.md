# Chapiana - Real-Time Chat & Video Call Application

<div align="center">

**Chapiana** (ቻጲና) - Kenyan Swahili slang meaning **"Talking With Each Other or Let's Talk"**

A modern, scalable real-time chat and video call application built with Django Channels, WebSockets, and a distributed architecture.

[Features](#key-features) • [Architecture](#architecture-overview) • [Getting Started](#getting-started) • [Contributing](#contributing) • [License](#license)

</div>

## Overview

Chapiana is a fully functional real-time chat and video call application designed for seamless instant messaging and calls. Built with a scalable backend architecture and an intuitive frontend interface, it supports:

- **One-on-One Messaging** - Private conversations between users
- **Group Chats** - Dynamic group discussions with multiple participants  
- **Video Calls** - Real-time video communication with WebSocket support
- **Live Status Updates** - Online/offline presence tracking
- **Message Persistence** - Complete chat history across sessions
- **Real-Time Notifications** - Instant alerts for new messages and calls

The system ensures efficient message delivery using WebSockets, providing a smooth real-time communication experience optimized for high performance and scalability.

## Tech Stack

- Django 
- Django Channels 
- WebSockets 
- PostgreSQL 
- Redis 
- Celery 
- Docker 
- NGINX

## Communication Mechanism

Chapiana uses a **Channel Layer** architecture that enables efficient multi-consumer communication.

### How It Works

1. **Channel**
A unique mailbox for each consumer instance, automatically generated for every WebSocket connection

2. **Group**
A collection of related channels identified by name, allowing broadcast messaging to multiple participants

3. **Channel Layer**
Backed by Redis, manages channels and groups for efficient message distribution

### Chat Room Communication

When multiple users join the same chat room:
1. Each user's `ChatConsumer` instance gets a unique channel name
2. All consumers in the same room add their channels to a group named after that room
3. Messages sent to the group are automatically broadcast to all channels in it
4. This enables seamless real-time communication between all room participants

### Background Task Processing

Chapiana uses **Celery** with Redis as the message broker to handle:
- Asynchronous notification tasks
- Video call retry mechanisms
- Background job processing without blocking WebSocket connections
- Scalable task distribution across multiple workers

This architecture ensures:
- Low-latency real-time messaging
- Reliable message delivery
- Scalable to multiple server instances
- Efficient resource utilization


## Key Features

1. **Instant Messaging**
   - Real-time chat powered by **WebSockets** and **Django Channels** for minimal latency
   - Support for text-based communication with emoji support

2. **User Authentication & Management**
   - Secure registration, login, and authentication using Django's built-in system
   - User profile management and profile editing
   - Friend request system for connecting users

3. **Responsive Design**
   - Clean and intuitive UI built with Django Templates
   - Styled with CSS and TailwindCSS for responsive experience
   - Works seamlessly across desktop and mobile devices

4. **One-on-One & Group Chats**
   - Private conversations between users
   - Dynamic group chats with user management
   - Category-based chat rooms (by country and user packages)

5. **Real-Time Interactions**
   - Typing indicators showing when users are typing
   - Read receipts for message delivery confirmation
   - Message delivery status updates

6. **Online Status Tracking**
   - Real-time online/offline presence indicators
   - Last seen timestamps for users
   - User availability status

7. **Notifications**
   - Instant alerts for new messages
   - Video call notifications with retry mechanism
   - Background task handling with Celery

8. **Message History & Search**
   - Complete message persistence in PostgreSQL
   - Search and filter chat history
   - Quick access to past conversations

9. **Video Call Support**
   - Real-time video call notifications
   - Call status tracking (pending, accepted, rejected, missed)
   - Celery-based notification retry system

10. **Scalable Architecture**
    - Designed for high performance and distributed deployments
    - Multi-process WebSocket handling
    - Redis for channel layer communication
    - Celery workers for background tasks
    - Support for Amazon S3 for media storage

## Architecture Overview

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Browser)                     │
│              Django Templates + JavaScript                  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API + WebSocket
          ┌──────────────┴──────────────┐
          │                             │
    ┌─────▼────────┐            ┌──────▼──────┐
    │  Gunicorn    │            │ ASGI Server │
    │  (REST API)  │            │ (WebSocket) │
    └─────┬────────┘            └──────┬──────┘
          │                            │
          └──────────────┬─────────────┘
                         │
    ┌────────────────────┴──────────────────────────┐
    │            Django Application                 │
    │  - Models, Views, Consumers, Serializers      │
    └────────────────────┬──────────────────────────┘
                         │
    ┌────────────────────┴──────────────┬───────────────────┐
    │                                   │                   │
┌──▼────────────┐             ┌────────▼─────┐       ┌──────▼─────┐
│  PostgreSQL   │             │    Redis     │       │   Celery   │
│  (Messages,   │             │  (Channels,  │       │   (Async   │
│   Users)      │             │   Cache)     │       │    Tasks)  │
└───────────────┘             └──────────────┘       └────────────┘
```

### Data Flow for a Message

1. **User sends message** → Frontend sends POST to REST API
2. **Django saves message** → Message stored in PostgreSQL
3. **WebSocket notification** → Message ID broadcasted via Channel Layer
4. **Real-time update** → All participants receive notification
5. **Frontend fetches message** → GET request to API to download full message
6. **Message displayed** → UI updates with new message

### Application Layers

**Presentation Layer**
- Consumes logic from the Use Case Layer
- Renders views via Swagger, ReDoc, or HTML templates
- Handles user interactions and responses

**Application Layer**
- Core application logic
- Views, ViewSets, Serializers
- WebSocket Consumers
- Models and Database Queries

**Domain Layer**
- Business logic independent of frameworks
- Data validation and transformation
- Core application rules

**Infrastructure Layer**
- Database access (PostgreSQL)
- Redis communication
- File storage (S3)
- External service integrations

## Patterns Used

1. **12 Factor App**

The project has been structured as a [12 factor app](https://12factor.net/). 

2. **Unit of Work Pattern**

This pattern coordinates the writing out of changes made to objects using the 
[repository pattern](https://dotnettutorials.net/lesson/unit-of-work-csharp-mvc/#:~:text=The%20Unit%20of%20Work%20pattern,or%20fail%20as%20one%20unit).

## Scaling

**Requests**

"Because Channels takes Django into a multi-process model, you no longer run everything in one process along with a WSGI server (of course, you’re still free to do that if you don’t want to use Channels). Instead, you run one or more interface servers, and one or more worker servers, connected by that channel layer you configured earlier."

In this case, I'm using the In-Memory channel system, but could be changed to the Redis backend to improve performance and spawn multiple workers in a distributed environment.

Please take a look at the link below for more information: https://channels.readthedocs.io/en/latest/introduction.html

## SSL Certificates

For production, replace nginx/ssl/cert.pem and nginx/ssl/key.pem with **Let’s Encrypt certificates.**

Run the following commands to generate a self-signed certificate for local testing:

```mkdir -p nginx/ssl```

```openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes```

## Running the Containers

```docker-compose up --build -d```

Now, Chapiana + Gunicorn runs behind NGINX, with SSL support and static file handling.


## Tech Stack

### Backend Services
- **Django 4.x+**: Web framework with REST API support
- **Django Channels**: WebSocket for real-time communication
- **PostgreSQL**: Primary database with indexing
- **Redis**: Message broker and caching layer
- **Celery**: Asynchronous task processing
- **Gunicorn**: WSGI production server
- **NGINX**: Reverse proxy and static file serving

### Frontend Stack  
- Django Templates, JavaScript, CSS/Tailwind

## User Flow

1. Sign up/login → 2. Edit profile → 3. Connect with friends → 4. Start chatting → 5. Video calls (coming)

## Getting Started

### Prerequisites

- **Python 3.12+** 
- **Redis Server**
- **PostgreSQL 12+** or SQLite for development
- **Virtual environment**

### Quick Installation

```bash
# 1. Clone & enter directory
git clone https://github.com/BiKodes/chapiana.git && cd chapiana

# 2. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements/base.txt

# 4. Setup environment
cp env.example.sh .env && nano .env

# 5. Setup database
python manage.py migrate && python manage.py createsuperuser

# 6. Start Redis
redis-server &

# 7. Run development server
python manage.py runserver
```

Navigate to `http://localhost:8000` to access the application.

### Docker Deployment (Recommended)

```bash
docker-compose up --build
docker-compose exec web python manage.py createsuperuser
```

### Production Deployment

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 src.config.wsgi:application

daphne -b 0.0.0.0 -p 8001 src.config.asgi:application

celery -A src.config worker -l info
```

## Important Notes

### Redis Required

```bash
redis-cli ping             
redis-server               
```

### Project Structure

```
chapiana/
├── src/
│   ├── accounts/          # User authentication
│   ├── chat/              # Chat functionality
│   ├── common/            # Shared utilities
│   ├── config/            # Django config
│   └── templates/         # HTML templates
├── requirements/          # Python dependencies
├── nginx/                 # Web server config
├── docker-compose.yml     # Docker services
└── README.md              # Documentation
```

### Testing

```bash
pytest                   
pytest tests/chat/ 
pytest --cov=src    
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request with a detailed description of your changes.

See [CONTRIBUTING.rst](CONTRIBUTING.rst) for detailed guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

1. Special thanks to the Django community for providing an excellent framework and resources
2. Inspired by modern chat applications like Slack, Discord, and WhatsApp
3. Django Channels team for making real-time communication in Django accessible

## Contact & Support

If you have any questions, suggestions, or feedback:

- **GitHub Issues**: [Report bugs or request features](https://github.com/BiKodes/chapiana/issues)
- **GitHub Profile**: [BiKodes](https://github.com/BiKodes)
- **Email**: bikocodes@gmail.com


## Todos & Roadmap

### Phase 1 (Foundation)
- [x] Setup Django project structure - DONE
- [x] Configure PostgreSQL database - DONE
- [x] Implement user authentication system - DONE
- [x] Create user profile models - DONE
- [x] Setup Django Channels for WebSockets - DONE

### Phase 2 (Core Chat Features)
- [ ] Implement real-time one-on-one messaging - PENDING
- [ ] Add read receipts (message delivered/read status) - PENDING
- [ ] Implement typing indicators - PENDING
- [ ] Create group chat functionality - PENDING
- [ ] Add message search and filtering - PENDING
- [ ] Implement user online/offline status tracking - PENDING
- [ ] Add last seen timestamp functionality - PENDING
- [ ] Create notification system for new messages - PENDING

### Phase 3 (Advanced Messaging Features)
- [ ] Implement video call notifications - PENDING
- [ ] Add message reactions and emoji support - PENDING
- [ ] Create message editing capability - PENDING
- [ ] Implement message deletion (with soft delete) - PENDING
- [ ] Add file and media sharing (images, videos, documents) - PENDING
- [ ] Implement message encryption (optional) - PENDING
- [ ] Add message forwarding - PENDING
- [ ] Create message pins/favorites - PENDING

### Phase 4 (User Experience)
- [ ] Improve UI/UX design - PENDING
- [ ] Mobile responsive improvements - PENDING
- [ ] Add dark mode support - PENDING
- [ ] Implement PWA features - PENDING
- [ ] Optimize frontend JavaScript - PENDING
- [ ] Improve accessibility (A11y) - PENDING
- [ ] Add animated transitions - PENDING
- [ ] Create better chat UI components - PENDING

### Phase 5 (Performance & Optimization)
- [ ] Performance tuning and benchmarking - PENDING
- [ ] Database query optimization and indexing - PENDING
- [ ] Implement query result caching - PENDING
- [ ] Redis memory optimization - PENDING
- [ ] Load testing and stress testing - PENDING
- [ ] Optimize WebSocket message size - PENDING
- [ ] Implement connection pooling - PENDING
- [ ] Profile and optimize hot paths - PENDING

### Phase 6 (Testing & Documentation)
- [ ] Comprehensive unit tests (target 80% coverage) - PENDING
- [ ] Integration tests for WebSocket consumers - PENDING
- [ ] API endpoint tests and validation - PENDING
- [ ] WebSocket stress testing - PENDING
- [ ] Architecture documentation - PENDING
- [ ] API documentation with Swagger/OpenAPI - PENDING
- [ ] Deployment guides and runbooks - PENDING
- [ ] Contributing guidelines - PENDING
- [ ] Code quality standards documentation - PENDING

### Phase 7 (Security & Reliability)
- [ ] Add CSRF protection validation - PENDING
- [ ] Implement rate limiting for API endpoints - PENDING
- [ ] Add two-factor authentication (2FA) - PENDING
- [ ] Implement message encryption (E2E) - PENDING
- [ ] Add input validation and sanitization - PENDING
- [ ] Implement audit logging - PENDING
- [ ] Add security headers - PENDING
- [ ] Regular security audits - PENDING
- [ ] Data privacy compliance (GDPR, etc.) - PENDING

### Phase 8 (DevOps & Deployment)
- [ ] Docker and Docker Compose setup (in progress) - IN PROGRESS
- [ ] NGINX configuration with SSL/TLS - PENDING
- [ ] Database backup and restore strategies - PENDING
- [ ] Monitoring and alerting setup - PENDING
- [ ] Logging aggregation (ELK stack optional) - PENDING
- [ ] Production deployment guide - PENDING
- [ ] Database migration strategies - PENDING
- [ ] Zero-downtime deployment setup - PENDING
- [ ] CI/CD pipeline (GitHub Actions) - PENDING
- [ ] Automated testing in CI/CD - PENDING

### Phase 9 (Scalability & Infrastructure)
- [ ] Implement database read replicas - PENDING
- [ ] Add Redis clustering - PENDING
- [ ] Setup Celery distributed workers - PENDING
- [ ] Implement message queue prioritization - PENDING
- [ ] Add load balancing - PENDING
- [ ] Horizontal scaling guide - PENDING
- [ ] Database sharding strategy - PENDING
- [ ] Cache invalidation strategy - PENDING
- [ ] WebSocket connection pooling - PENDING

### Phase 10 (Video Calling (Future))
- [ ] Implement video call signaling - PENDING
- [ ] Add WebRTC integration - PENDING
- [ ] Video codec selection - PENDING
- [ ] Call quality adaptation - PENDING
- [ ] Screen sharing support - PENDING
- [ ] Recording functionality - PENDING
- [ ] Call history tracking - PENDING
- [ ] Call analytics - PENDING

### Phase 11 (Analytics & Monitoring)
- [ ] User activity analytics - PENDING
- [ ] Message volume metrics - PENDING
- [ ] Performance metrics dashboard - PENDING
- [ ] Error tracking (Sentry) - PENDING
- [ ] Application performance monitoring (APM) - PENDING
- [ ] User engagement metrics - PENDING
- [ ] Call duration and quality metrics - PENDING

### Phase 12 (Admin & Management)
- [ ] Enhanced admin dashboard - PENDING
- [ ] User management interface - PENDING
- [ ] Chat moderation tools - PENDING
- [ ] Message filtering and rules - PENDING
- [ ] User suspension/banning - PENDING
- [ ] Analytics dashboard - PENDING
- [ ] System health monitoring - PENDING
- [ ] Bulk operations support - PENDING

### Known Issues & Improvements Needed
- [ ] Improve error handling in WebSocket consumers - PENDING
- [ ] Add comprehensive error logging - PENDING
- [ ] Implement connection retry logic - PENDING
- [ ] Better handling of disconnections - PENDING
- [ ] Improve code documentation and docstrings - PENDING
- [ ] Refactor large consumer files - PENDING
- [ ] Add integration tests - PENDING
- [ ] Improve frontend code organization - PENDING
- [ ] Optimize database queries (N+1 problems) - PENDING
- [ ] Add request/response validation middleware - PENDING
- [ ] Implement request throttling - PENDING
- [ ] Better exception handling patterns - PENDING

### Quick Wins (Low effort, high value)
- [ ] Add missing docstrings to models - PENDING
- [ ] Create API documentation - PENDING
- [ ] Add Docker health checks - PENDING
- [ ] Implement database indexes for common queries - PENDING
- [ ] Add more test fixtures - PENDING
- [ ] Create development setup script - PENDING
- [ ] Add pre-commit hooks - PENDING
- [ ] Create API response standards - PENDING

<div align="center">

[⬆ Back to Top](#chapiana---real-time-chat--video-call-application)

</div>


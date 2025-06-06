# Overview

**Chapiana** is Kenyan Swahili slang meaning **"Talking With Each Other or Lets Talk".** It is a fully functional real 
time chat and video call application designed for seamless and instant messaging and calls. Built with a scalable backend architecture and 
an intuitive frontend interface, this application supports one-on-one messaging, group chats, and live status updates. 

The system ensures efficient message delivery using WebSockets, providing a smooth real time communication experience.

## Communication Mechanism
The channel layer is a communication system that allows multiple consumer instances to talk with each other.

A channel layer offers several key abstractions:

**Channel**

A mailbox for sending messages. Messages can be sent to a channel using its name. Every consumer instance has a unique 
channel name, generated automatically.

**Group**

A collection of related channels identified by a name. Participants can add or remove channels from the group using the 
group's name. Messages sent to the group are broadcasted to all channels in it.

In the context of a chat application, the goal is to enable multiple instances of ChatConsumer within the same chat room 
to interact. This is achieved by having each ChatConsumer add its channel to a group named after the room. 
By doing so, messages sent to the group are received by all ChatConsumers in that room.

To implement this, a channel layer that uses Redis as its underlying storage mechanism is used. Redis provides the 
infrastructure to manage these channels and groups, enabling efficient message distribution among participants.

**Retries**

We are using Celery to handle all retries on tasks failures. This also offer an additional anecdote to our systems scalability by offlaoding work from it to background workers. We notify users of an incoming call in real time and retry missed notifiactions.


## Key Features

1. **Instant Messaging**

  Real time chat functionality powered by **WebSockets** and **Django Channels** for minimal latency.

2. **User Authentication**
  
  Secure user registration, login, and authentication using Django's built-in authentication system.

3. **Responsive Design**

  Clean and intuitive user interface built with Django Templates and styled with CSS and TailwindCSS for a responsive 
  experience.
  
4. **One-on-One & Group Chats**

  Private conversations and group discussions with dynamic user management.

5. **Typing Indicators & Read Receipts**

  Real time feedback on message interactions.

6. **Online Status**

  Track the online/offline status of users in real time.

7. **Notifications**

  Instant alerts for new messages and mentions.

8. **Message History & Persistence**

  Stored chat history for seamless access across sessions.

9. **Search and Connect**

Find and connect with users quickly.

10. **Scalability**

  Optimized for high performance and scalable deployments on Amazon S3

11. **Scalable Architecture** 

  Built with Django's robust backend and scalable WebSocket integration for handling growing user bases.

## Architecture

When a user logs in, the frontend downloads the user list and opens a Websocket connection to the server (notifications channel).

When a user selects another user to chat, the frontend downloads the latest 15 messages (see settings) they've exchanged.

When a user sends a message, the frontend sends a POST to the REST API, then Django saves the message and notifies the users involved using the Websocket connection (sends the new message ID).

When the frontend receives a new message notification (with the message ID), it performs a GET query to the API to download the received message.


**This project impliments the follwing layers:**

1. **Presentation Layer**

This represents logic that consume the user logic from the Usecase Layer and renders to the view. Here you can 
choose to render the view in either ```swagger``` or ```redoc.```

2. **Application Layer**

The application specific logic lives here, this includes interfaces, views, serializers, models etc.

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

1. **Backend**

  Python (Django, Django Channels), Redis, PostgreSQL

2. **Frontend**

  Django Templates for rendering dynamic HTML pages and JavaScript.

3. **WebSockets**

  Django Channels for real time communication

4. **Celery**

  We are using Celery to manage Video call notification status.

  ```bash
        [ Chapiana program ]
                |
                v
      (Chapiana Task sent to queue)
                |
                v
            [ Redis ]  <--- Message Broker
                |
                v
         [ Celery Worker ] ---> Runs notifications task in background
  ````

5. **Authentication**

  Django's built-in authentication system for secure user management.

6. **Styling**

  CSS and Tailwind CSS for a modern and polished design.

7. **Database**

  PostgreSQL for storing user data and chat history. If more performance is required, 
  a PostgreSQL cluster / shard could be deployed.

  PD: I'm using indexes to improve performance.

8. **Docker Volumes**

  It is to persist database data.

9. **Nginx**

  Chapiana configures NGINX  as a reverse proxy for performance to:

  - Proxy requests to Django + Gunicorn.

  - Serve static and media files.

  - Enable SSL (HTTPS).

10. **Gunicorn**

  We are using using Gunicorn instead of Django’s built-in server for production.

11. **Deployment**

  Docker, Nginx, and Gunicorn for production readiness

## User Flow

1. **Sign Up or Log In**

Create your account or log in securely.

2. **Dashboard Access**

  i. Edit your profile and manage settings.
  ii. Search and add friends effortlessly.

3. **Friend Requests**

Send, accept, or decline friend requests.

4. **Start Chatting**

Engage in seamless, real-time conversations.

## Getting Started

### Prerequisites

Python 3.12 installed on your machine.

Basic knowledge of Python, Django, and Django Templates.

Installation
1. **Clone the Repository**

```git clone https://github.com/your-username/chapiana.git```

```cd chapiana```

2. **Create a Virtual Environment**

```python -m venv venv```

```source venv/bin/activate```

**_On Windows_**
```venv\Scripts\activate```

3. **Install Dependencies**

```pip install -r requirements.txt```

4. **Set Up the Database**
Apply migrations to set up the database:

```python manage.py migrate```

5. **Set Up Environment Variables**
Create a .env file in the root directory and add the necessary environment variables:

```SECRET_KEY=your_django_secret_key```

```DEBUG=True```

6. **Run the Application**
Start the Django development server:

```python manage.py runserver```

7. **Access the Application**
Open your browser and navigate to ```http://127.0.0.1:8000``` to start using the chat application.

8. **Run Gunicorn to Serve Chapiana**
Navigate to Chapiana's project’s root directory and run:

```gunicorn --workers 3 --bind 0.0.0.0:8000 src.wsgi:application```


  **Breakdown**

  - --workers 3 → Runs 3 worker processes (adjust based on server resources).

  - --bind 0.0.0.0:8000 → Binds to port 8000.

  - src.wsgi:application → Uses WSGI entry point.


### Project Structure

```bash
chapiana/
├── chat/                  # Django app for chat functionality
│   ├── templates/         # Django templates for chat UI
│   ├── consumers.py       # WebSocket consumers for real-time messaging
│   ├── routing.py         # WebSocket routing configuration
│   └── ...
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables
└── ...
```

### Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bugfix.

3. Commit your changes and push to your branch.

4. Submit a pull request with a detailed description of your changes.

### Design Note

**Chapiana** is majorly focused on the backend functionality and lacks a production grade user interface design.

This design choice allows developers to focus solely on the backend and the integration of Django Channels for 
real-time communication. 

As a result, **Chapiana** serves as a great educational resource and a starting point for those looking to learn 
about Django, Django Channels, and real-time communication.


### Performance

> [!NOTE]
> It is better to use the **virtualenvironment** when installing libraries and running the project. 


> [!WARNING]
> Have **redis** installed on the system before running. <br>
> download and install [redis for windows](https://github.com/tporadowski/redis/releases) and to `cmd` type `redis-server` to run the redis.

### Resources
1. [Django Tutorial - Corey Schafer](https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p) 
2. [Django Channels - RealPython](https://realpython.com/getting-started-with-django-channels/)
3. [Django Channels](https://channels.readthedocs.io/)
4. [Django Channels and WebSockets oversimplified - Dennis Ivy](https://www.youtube.com/watch?v=cw8-KFVXpTE)
5. [Token Auth middleware ideas](https://gist.github.com/rluts/22e05ed8f53f97bdd02eafdf38f3d60a)

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgments

1. Special thanks to the Django community for providing an excellent framework and resources.

2. I was inspired by modern chat applications like Slack, Discord, and WhatsApp.

### Contact

If you have any questions, suggestions, or feedback, feel free to reach out:

1. **GitHub**
  [BiKodes](https://github.com/BiKodes)

2. **Email** 
  bikocodes@gmail.com


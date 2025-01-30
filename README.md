# Overview

**Chapiana** is a fully functional real time chat application designed for seamless and instant messaging. Built with a scalable backend architecture and an intuitive frontend interface, this application supports one-on-one messaging, group chats, and live status updates. 

The system ensures efficient message delivery using WebSockets, providing a smooth real time communication experience.

## Key Features

- **Instant Messaging**

  Real time chat functionality powered by **WebSockets** and **Django Channels** for minimal latency.

- **User Authentication**
  
  Secure user registration, login, and authentication using Django's built-in authentication system.

- **Responsive Design**

  Clean and intuitive user interface built with Django Templates and styled with CSS and TailwindCSS for a responsive experience.
  
- **One-on-One & Group Chats**

  Private conversations and group discussions with dynamic user management.

- **Typing Indicators & Read Receipts**

  Real time feedback on message interactions.

- **Online Status**

  Track the online/offline status of users in real time.

- **Notifications**

  Instant alerts for new messages and mentions.

- **Message History & Persistence**

  Stored chat history for seamless access across sessions.

- **Scalability**

  Optimized for high performance and scalable deployments on Amazon S3

- **Scalable Architecture** 

  Built with Django's robust backend and scalable WebSocket integration for handling growing user bases.

## Tech Stack

- **Backend**

  Python (Django, Django Channels), Redis, PostgreSQL

- **Frontend**

  Django Templates for rendering dynamic HTML pages.

- **WebSockets**

  Django Channels for real time communication

- **Authentication**

  Django's built-in authentication system for secure user management.

- **Styling**

  CSS and Tailwind CSS for a modern and polished design.

- **Database**

  PostgreSQL for storing user data and chat history.

- **Deployment**

  Docker, Nginx, and Gunicorn for production readiness

## Getting Started

### Prerequisites

- Python 3.12 installed on your machine.

- Basic knowledge of Python, Django, and Django Templates.

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

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgments

- Special thanks to the Django community for providing an excellent framework and resources.

- I was inspired by modern chat applications like Slack, Discord, and WhatsApp.

### Contact

If you have any questions, suggestions, or feedback, feel free to reach out:

- **GitHub**
  [BiKodes](https://github.com/BiKodes)

- **Email** 
  bikocodes@gmail.com


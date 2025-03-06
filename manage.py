#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.local")
    os.environ.setdefault("DJANGO_CONFIGURATION", "LOCAL")

    try:
        from configurations.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

'''
The design and operation process of chapiana is such that the address of the 
chat room is received on the index page. (if the chat room is available, it 
will be entered, and if it is not available, the chat room will be created). 

After the person enters the room, you can communicate with the people who have 
entered the chat room.

According to the picture, when a message is sent from the mahdi user, the 
message is sent to the server through websocket. The server saves the message 
once in the database and sends the same message again to the mahdi user and 
other users without the need for a request. All messages are received in the 
form of json through the client, and the main part of designing and displaying 
the messages is the responsibility of the client.

django channels is designed in the form of a messenger application whose client 
is javascript and its back-end has created a websocket-based connection with django.
In addition to the Super Chat section, the dashboard section is intended for users,
which makes the sections and settings of the user's account accessible. 

Basically, it shows the number of user messages, the number of chat rooms in which 
the user is present, along with the deletion and display section of the chat room, 
the last login to the account and the date of registration. 

Other sections of this dashboard include the following sections:

    - Changing the password.

    - User account settings and user profile editing.

    - Logging out of the user account.

In fact, the main part is the user dashboard, which can be accessed only by logging 
into the user account.

Note:

    - It is better to use the virtualenvironment when installing libraries and running
    the project.

Warning:

        - Have redis installed on the system before running.
        - Download and install redis for windows and to cmd type redis-server to run the redis.
'''

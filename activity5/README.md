# Concurrent Echo Server and Client

## Overview
This project combines a concurrent echo server and a client using Python's socket and threading libraries. The server is capable of  handling multiple client connections simultaneously, echoing back any messages it receives. The client can connect to the server, send messages, and receive echoes of those messages.

+ The server program listens for incoming connections from clients and handles each connection in a separate thread, allowing multiple clients to communicate with the server concurrently.
+ The client program connects to the server, sends messages entered by the user, and displays the server's responses.

## Setup and Execution
+ Before starting make sure your [Python](https://www.python.org/) is up-to-date.

### To run the server:
1. Download the repository
2. Open a terminal or command prompt window
3. Navigate to the directory containing `server.py`
4. Run the `server.py`
6. The server will start and listen for client connections on localhost and port 65432 (default).


### To run the client:
1. Ensure the server is running and listening for connections.
2. Open a new terminal or command prompt window.
3. Navigate to the directory containing `client.py`.
4. Run the `client.py`
5. Once connected, follow the prompts to enter messages. The server's responses will be displayed.
6. To exit, type `quit` at the message prompt.

This concurrent echo server and client application demonstrates basic network programming concepts in Python, including socket communication and threading for concurrency. Feel free to modify and extend the functionality as needed for your purposes.
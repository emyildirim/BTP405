import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

# Handle a single client connection and listen for messages
def handle_client(connection, address):
    print(f'Connected by {address}')
    try:
        # Continuously listen for messages
        while True:
            message = connection.recv(1024)
            if not message or message.decode() == 'quit':
                break
            # Echo the received message back to client
            print(f'Received from {address}: {message.decode()}')
            connection.sendall(message)
    finally:
        # Close the connection when 'quit' is received or if client disconnects
        print(f'Client disconnected : {address}')
        connection.close()

# Start the server and listen for incoming connections
def start_server(host=HOST, port=PORT):
    
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server started, listening on {host}:{port}')
        
        # Continuously listen for connections and create a new thread for each connected client.
        while True:
            connection, address = s.accept()
            thread = threading.Thread(target=handle_client, args=(connection, address))
            thread.start()

if __name__ == "__main__":
    start_server()

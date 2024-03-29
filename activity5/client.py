import socket

HOST = '127.0.0.1'
PORT = 65432

# Start the client and connect to the server
def start_client(host=HOST, port=PORT):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # Connect to the server
            s.connect((host, port))
            print("Connected to the server.")
            
            # Receive user input and send to server
            while True:
                message = input("Enter message: ")
                s.sendall(message.encode())
                if message == 'quit':
                    break
                info = s.recv(1024)
                print(f'Received from server: {info.decode()}')
    except ConnectionRefusedError:
        print("Could not connect to the server at the specified host and port.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_client()

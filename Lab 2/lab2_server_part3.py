import socket
import threading

clients = {}  # Dictionary to store client sockets and their usernames

def handle_client(client_socket, client_address):
    """Handles communication with a single client."""
    try:
        # Receive username from client
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"{username} has connected from {client_address}.")

        # Notify others about the new connection
        broadcast_message(f"{username} has joined the chat!", client_socket)

        # Handle incoming messages
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{username}: {message}")
                broadcast_message(message, client_socket)
            else:
                break
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        # Handle client disconnection
        if client_socket in clients:
            print(f"{username} has disconnected.")
            broadcast_message(f"{username} has left the chat.", client_socket)
            del clients[client_socket]
            client_socket.close()

def broadcast_message(message, sender_socket):
    """Sends a message to all connected clients except the sender."""
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")

def start_server():
    """Starts the server and listens for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server started. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_server()

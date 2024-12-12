import socket
import threading

# Global list to keep track of connected clients
clients = []

def handle_client(client_socket, client_address):
    """Handles communication with a connected client."""
    print(f"New connection from {client_address}")
    client_socket.send("Welcome to the chat server!".encode('utf-8'))
    
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:  # Client disconnected
                break
            print(f"Message from {client_address}: {message}")
            
            # Broadcast the message to other clients
            broadcast_message(client_socket, f"[{client_address}] {message}")
        except Exception as e:
            print(f"Error with client {client_address}: {e}")
            break
    
    # Remove the client and close the connection
    remove_client(client_socket)
    client_socket.close()
    print(f"Connection with {client_address} closed.")

def broadcast_message(sender_socket, message):
    """Sends a message to all connected clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting to a client: {e}")

def remove_client(client_socket):
    """Removes a client from the global list."""
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    """Starts the chat server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 12345)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"Server listening on {server_address}")
    
    while True:
        # Accept new client connections
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        
        # Start a new thread for the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()

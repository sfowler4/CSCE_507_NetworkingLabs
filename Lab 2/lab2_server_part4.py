import socket
import threading

clients = {}  # Dictionary to store client_name: client_socket

def handle_client(client_socket, client_name):
    # Add the client to the clients dictionary
    clients[client_name] = client_socket
    print(f"{client_name} joined the chat from {client_socket.getpeername()}")

    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break  # Client disconnected
            
            print(f"{client_name} sent: {message}")
            
            # Extract recipient and message content
            try:
                recipient_name, msg_content = message.split(":", 1)
            except ValueError:
                client_socket.send("Message format error. Use recipient_name:message".encode())
                continue

            # Forward message to the recipient
            if recipient_name in clients:
                recipient_socket = clients[recipient_name]
                recipient_socket.send(f"{client_name}: {msg_content}".encode())
            else:
                client_socket.send(f"{recipient_name} is not connected.".encode())
                
    except Exception as e:
        print(f"Error with {client_name}: {e}")
    finally:
        # Cleanup after disconnection
        print(f"{client_name} has disconnected.")
        del clients[client_name]
        client_socket.close()

def start_server(server_ip, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)  # Allow up to 5 clients to connect

    print(f"Server started at {server_ip}:{server_port}")
    
    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # Ask for client name
        client_name = client_socket.recv(1024).decode().strip()
        print(f"Client name received: {client_name}")

        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_thread.daemon = True  # Ensure threads are terminated when the server shuts down
        client_thread.start()

if __name__ == "__main__":
    server_ip = "192.168.1.15"  # Replace with your machine's IP
    server_port = 8020
    start_server(server_ip, server_port)

import socket
import threading

# Server setup
server_ip = '10.231.239.100'
server_port = 8020
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

# Store connected clients
clients = {}

def handle_client(client_socket, client_address):
    client_name = client_socket.recv(1024).decode()  # Receive client's name/ID
    clients[client_name] = client_socket
    print(f"{client_name} joined from {client_address}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"{client_name} says: {message}")
                recipient_name, msg_content = message.split(":", 1)
                
                if recipient_name in clients:
                    clients[recipient_name].send(f"{client_name}: {msg_content}".encode())
                else:
                    client_socket.send(f"{recipient_name} not connected.".encode())
            else:
                break
        except:
            break

    # Clean up after disconnection
    print(f"{client_name} disconnected.")
    del clients[client_name]
    client_socket.close()

def start_server():
    print(f"Server running on {server_ip}:{server_port}")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

start_server()

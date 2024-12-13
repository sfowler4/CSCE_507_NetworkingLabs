import socket
import threading

clients = {}  # Dictionary to store client_name: client_socket
groups = {} # Dictionary to hold groups

def handle_client(client_socket, client_address):
    client_name = client_socket.recv(1024).decode()
    clients[client_name] = client_socket
    print(f"{client_name} joined from {client_address}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith("/creategroup"):
                _, group_name = message.split(" ", 1)
                if group_name not in groups:
                    groups[group_name] = [client_name]
                    client_socket.send(f"Group '{group_name}' created.".encode())
                else:
                    client_socket.send(f"Group '{group_name}' already exists.".encode())
            
            elif message.startswith("/addtogroup"):
                _, group_name, new_member = message.split(" ", 2)
                if group_name in groups and client_name in groups[group_name]:
                    if new_member in clients:
                        groups[group_name].append(new_member)
                        client_socket.send(f"{new_member} added to group '{group_name}'.".encode())
                    else:
                        client_socket.send(f"{new_member} is not connected.".encode())
                else:
                    client_socket.send(f"You do not have permission to modify group '{group_name}'.".encode())
            
            elif message.startswith("/groupmessage"):
                _, group_name, msg_content = message.split(" ", 2)
                if group_name in groups and client_name in groups[group_name]:
                    for member in groups[group_name]:
                        if member != client_name and member in clients:
                            clients[member].send(f"[{group_name}] {client_name}: {msg_content}".encode())
                else:
                    client_socket.send(f"You are not a member of group '{group_name}'.".encode())
            
            else:
                client_socket.send("Unknown command.".encode())

        except:
            break

    # Clean up after disconnection
    del clients[client_name]
    for group in groups.values():
        if client_name in group:
            group.remove(client_name)
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

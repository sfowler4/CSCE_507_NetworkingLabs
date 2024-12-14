import socket
import threading

clients = {}  # Dictionary to store client_name: client_socket
groups = {}  # Dictionary to hold groups

group_lock = threading.Lock()  # Lock to ensure thread-safe access to groups

def handle_client(client_socket, client_name):
    print(f"{client_name} joined.")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.startswith("/creategroup"):
                _, group_name = message.split(" ", 1)
                with group_lock:
                    if group_name not in groups:
                        groups[group_name] = set()
                        groups[group_name].add(client_name)
                        client_socket.send(f"Group '{group_name}' created and you are added.".encode())
                    else:
                        client_socket.send(f"Group '{group_name}' already exists.".encode())

            elif message.startswith("/joingroup"):
                _, group_name = message.split(" ", 1)
                with group_lock:
                    if group_name in groups:
                        groups[group_name].add(client_name)
                        client_socket.send(f"You joined group '{group_name}'.".encode())
                    else:
                        client_socket.send(f"Group '{group_name}' does not exist.".encode())

            elif message.startswith("/addtogroup"):
                _, group_name, new_member = message.split(" ", 2)
                with group_lock:
                    if group_name in groups and client_name in groups[group_name]:
                        if new_member in clients:
                            groups[group_name].add(new_member)
                            client_socket.send(f"{new_member} added to group '{group_name}'.".encode())
                        else:
                            client_socket.send(f"{new_member} is not connected.".encode())
                    else:
                        client_socket.send(f"You do not have permission to modify group '{group_name}'.".encode())

            elif message.startswith("/groupmessage"):
                _, group_name, msg_content = message.split(" ", 2)
                with group_lock:
                    if group_name in groups and client_name in groups[group_name]:
                        for member in groups[group_name]:
                            if member != client_name and member in clients:
                                clients[member].send(f"[{group_name}] {client_name}: {msg_content}".encode())
                    else:
                        client_socket.send(f"You are not a member of group '{group_name}'.".encode())

            elif message.startswith("/sendfile"):
                _, group_name, filename = message.split(" ", 2)
                with group_lock:
                    if group_name in groups and client_name in groups[group_name]:
                        # Notify the group about the incoming file
                        for member in groups[group_name]:
                            if member != client_name and member in clients:
                                clients[member].send(f"[{group_name}] {client_name} is sending a file: {filename}".encode())
                        
                        # Receive file size
                        file_size = int(client_socket.recv(1024).decode())
                        print(f"Receiving file '{filename}' of size {file_size} bytes from {client_name}")

                        # Receive the file data
                        file_data = b""
                        received = 0
                        while received < file_size:
                            chunk = client_socket.recv(1024)
                            file_data += chunk
                            received += len(chunk)

                        # Send the file data to group members
                        for member in groups[group_name]:
                            if member != client_name and member in clients:
                                clients[member].send(f"STARTFILE {filename} {file_size}".encode())
                                clients[member].sendall(file_data)
                                clients[member].send(f"ENDFILE {filename}".encode())
                        print(f"File '{filename}' sent to group '{group_name}'")

                    else:
                        client_socket.send(f"You are not a member of group '{group_name}'.".encode())

            else:
                client_socket.send("Unknown command.".encode())

        except Exception as e:
            print(f"Error with {client_name}: {e}")
            break

    # Clean up after disconnection
    with group_lock:
        del clients[client_name]
        for group in groups.values():
            group.discard(client_name)
    client_socket.close()
    print(f"{client_name} disconnected.")

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
        if client_name in clients:
            client_socket.send("Name already in use. Disconnecting.".encode())
            client_socket.close()
            continue

        clients[client_name] = client_socket
        client_socket.send("Welcome to the server!".encode())

        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_thread.daemon = True  # Ensure threads are terminated when the server shuts down
        client_thread.start()

if __name__ == "__main__":
    server_ip = "192.168.1.15"  # Replace with your machines IP
    server_port = 8020
    start_server(server_ip, server_port)
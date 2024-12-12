import socketserver
import threading

# Dictionary to store connected clients
clients = {}

# Thread-safe lock for client dictionary
lock = threading.Lock()


class ChatHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive client's name
        client_name = self.request.recv(1024).decode()
        with lock:
            clients[client_name] = self.request
        print(f"{client_name} joined from {self.client_address}")

        try:
            while True:
                message = self.request.recv(1024).decode()
                if message:
                    print(f"{client_name} says: {message}")
                    recipient_name, msg_content = message.split(":", 1)

                    with lock:
                        if recipient_name in clients:
                            clients[recipient_name].sendall(f"{client_name}: {msg_content}".encode())
                        else:
                            self.request.sendall(f"{recipient_name} not connected.".encode())
                else:
                    break
        except Exception as e:
            print(f"Error handling {client_name}: {e}")
        finally:
            # Remove client on disconnect
            with lock:
                print(f"{client_name} disconnected.")
                del clients[client_name]
                self.request.close()


class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


# Server setup
if __name__ == "__main__":
    server_ip = "1982.168.1.15"  # Change as needed for deployment
    server_port = 8020

    with ChatServer((server_ip, server_port), ChatHandler) as server:
        print(f"Server running on {server_ip}:{server_port}")
        server.serve_forever()

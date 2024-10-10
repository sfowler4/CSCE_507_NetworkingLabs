# Import necessary libraries
import socket

# Client details
CLIENT_NAME = "Client of Sam K. Fowler, C00591626"

HOST = '10.231.249.19'  # Server's hostname or IP address
PORT = 8020             # Server's port

def start_client():
    # Get an integer input from the user
    while True:
        try:
            # Get user input
            client_number = int(input("Enter an integer between 1 and 100: "))

            # Establish connection to the server and send message
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((HOST, PORT))
                print("Connected to server!")

                # Create a message to send to the server
                message = f"{CLIENT_NAME} -  {client_number}"

                if not (1 <= client_number <= 100):
                    print("Invalid Input! Terminating server connection.")  # Give client message that server will be terminated
                    sock.sendall(message.encode('utf-8'))                   # Send invalid number so server knows to terminate
                    break

                print(f"Sending message to the server: {message}")
                sock.sendall(message.encode('utf-8'))       # Encode message to prep for sending

                # Wait for the server's response
                data = sock.recv(1024)                      # Give 1K buffer
                reply = data.decode('utf-8')                # Decode reply
                print(f"Server reply: {reply}")             # Print server reply

        # Exception cases for the try block
        except ValueError:
            print("Invalid input. Please enter an integer.")
            break

        except ConnectionResetError:
            print("The server has closed the connection.")
            break

        except Exception as e:
            print(f"An error has occurred: {e}")
            break

if __name__ == "__main__":
    start_client()

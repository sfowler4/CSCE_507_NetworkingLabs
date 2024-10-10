# Import necessary libraries
import socket
import random

# Create string to be given out upon reciept of the client
SERVER_NAME = "Server of Sam K. Fowler, for CSCE 513"

# Host IP used to connect to outside client
HOST = '10.231.249.19'

# Choose available port between 1024 and 65535
PORT = 8020

#Create function for starting the server
def server_start():

    # Create boolean variable for invalid input
    invalid_input = False

    # Creates socket and waits for connection to the client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"{SERVER_NAME} is waiting for a connection on {HOST}:{PORT}...")     # Print to inform that server has correctly created socket and is waiting for connection

        while True:
            conn, addr = sock.accept()
            with conn:
                print(f"Connected by {addr}")           # Print statement to show connection has taken place

                while True:                             # While loop to keep connection persistent until invalid number is sent

                    # data = conn.recv(1024)                  # Give 1K buffer
                    # if not data:                            # Check for data
                    #     break                               # break if no data received

                    # message = data.decode('utf-8')              # Decode data received and place in variable message
                    # print(f"Recieved message: {message}")       # Print message received from client

                    try:

                        data = conn.recv(1024)                  # Give 1K buffer
                        if not data:                            # Check for data
                            break                               # break if no data received

                        message = data.decode('utf-8')              # Decode data received and place in variable message
                        print(f"Recieved message: {message}")       # Print message received from client

                        client_name, client_number = message.split("-")                                 # Place client name and number in variables
                        client_number = int(client_number.strip())                                      # Remove whitespace from client number and cast to int for summing

                        if not (1 <= client_number <= 100):                                             # Check if number from client is invalid
                            print(f"Invalid number received: {client_number}. Terminating server.")     # Send message that server will be terminated due to invalid number
                            invalid_input = True                                                        # Set variable used to break out of server loop
                            break                                                                       # Terminate server if number from client is invalid
                        

                        # Server picks random number 1-100
                        SERVER_NUMBER = random.randint(1,100)

                        # Print information necessary about both client and server

                        print(f"Client's name: {client_name}")          # Print name sent by client
                        print(f"Client's number: {client_number}")      # Print number sent by client
                        print(f"Servers's name: {SERVER_NAME}")         # Print servers name
                        print(f"Server's number: {SERVER_NUMBER}")      # Print servers random number
                        print(f"Sum: {client_number + SERVER_NUMBER}")  # Print sum of client and server numbers


                        print("Sending message...")
                        reply = f"{SERVER_NAME}, {SERVER_NUMBER}"       # Define message to be sent to client
                        conn.sendall(reply.encode('utf-8'))             #Send response to client
                        print(f"Message sent: {reply}")

                    except Exception as e:
                        print(f"Error processing message: {e}")     # Error handling for message 
                        break                                       # Terminates if any exceptions take place

            if invalid_input:
                break
            print("Waiting for the next message...")        # Print to see that server is waiting on next message

            
        print("Connection Terminated.")     # Close connection if invalid number is entered by client


if __name__ == "__main__":
    server_start()         # Start server using defined function



import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import select
import sys

# Client setup
server_ip = '192.168.1.15'  # Update with your server's IP
server_port = 8020

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# GUI setup
class ChatClientGUI:
    def __init__(self, root, client_name):
        self.root = root
        self.client_name = client_name
        self.root.title(f"csce513fall24Msg Chat Client - {client_name}")  # Set window title to include the username
        
        # Chat history area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=50, height=15)
        self.chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Group entry
        tk.Label(self.root, text="Group:").grid(row=1, column=0, sticky='e')
        self.group_entry = tk.Entry(self.root, width=30)
        self.group_entry.grid(row=1, column=1, pady=5, padx=10)

        # Group buttons
        self.create_group_button = tk.Button(self.root, text="Create Group", command=self.create_group)
        self.create_group_button.grid(row=1, column=2, pady=5)

        self.join_group_button = tk.Button(self.root, text="Join Group", command=self.join_group)
        self.join_group_button.grid(row=2, column=2, pady=5)

        # Recipient entry
        tk.Label(self.root, text="Recipient:").grid(row=3, column=0, sticky='e')
        self.recipient_entry = tk.Entry(self.root, width=30)
        self.recipient_entry.grid(row=3, column=1, pady=5, padx=10)

        # Message input area
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.grid(row=4, column=0, columnspan=2, pady=5, padx=10)
        self.message_entry.bind("<Return>", self.send_message)  # Send on Enter key

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=4, column=2, pady=5)

        # Start receiving messages
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def display_message(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state='disabled')

    def create_group(self):
        group_name = self.group_entry.get().strip()
        if not group_name:
            messagebox.showwarning("Warning", "Group name cannot be empty.")
            return
        formatted_message = f"/creategroup {group_name}"
        client_socket.send(formatted_message.encode())
        self.display_message(f"Created group: {group_name}")

    def join_group(self):
        group_name = self.group_entry.get().strip()
        if not group_name:
            messagebox.showwarning("Warning", "Group name cannot be empty.")
            return
        formatted_message = f"/joingroup {group_name}"
        client_socket.send(formatted_message.encode())
        self.display_message(f"Joined group: {group_name}")

    def send_message(self, event=None):
        recipient = self.recipient_entry.get().strip()
        message = self.message_entry.get().strip()
        group_name = self.group_entry.get().strip()
        
        if not message:
            messagebox.showwarning("Warning", "Message cannot be empty.")
            return

        if group_name:  # Send message to group if group is specified
            formatted_message = f"/groupmessage {group_name} {message}"
            client_socket.send(formatted_message.encode())
            self.display_message(f"You (to {group_name}): {message}")
        elif recipient:  # Send private message
            formatted_message = f"{recipient}:{message}"
            client_socket.send(formatted_message.encode())
            self.display_message(f"You -> {recipient}: {message}")
        else:
            messagebox.showwarning("Warning", "Recipient or group must be specified.")
        
        self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while self.running:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    self.display_message(message)
                else:
                    self.running = False
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.running = False
                break

    def close_connection(self):
        self.running = False
        client_socket.close()
        self.root.destroy()

# Initialize client
client_name = input("Enter your name: ")
client_socket.send(client_name.encode())  # Send the client's name to the server

# Start GUI
root = tk.Tk()
app = ChatClientGUI(root, client_name)  # Pass the client name to the GUI class
root.protocol("WM_DELETE_WINDOW", app.close_connection)  # Close socket on window close
root.mainloop()

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Message entry area
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=10, pady=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        # Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.1.15', 8020)
        try:
            self.client_socket.connect(server_address)
            self.add_message("Connected to the server!")
        except Exception as e:
            self.add_message(f"Failed to connect: {e}")
            return

        # Start a thread to receive messages
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def add_message(self, message):
        """Adds a message to the chat display."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        """Sends a message to the server."""
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.add_message(f"Error sending message: {e}")

    def receive_messages(self):
        """Continuously receives messages from the server."""
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.add_message(message)
            except Exception as e:
                self.add_message(f"Error receiving message: {e}")
                break

# Main GUI loop
if __name__ == "__main__":
    root = tk.Tk()
    chat_client = ChatClient(root)
    root.mainloop()

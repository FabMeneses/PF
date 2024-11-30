import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

def ejecutar():
    class ChatServer:
        def __init__(self, root):
            self.root = root
            self.root.title("Servidor de Chat")
            self.root.configure(bg="#34495e")  # Fondo oscuro para la ventana principal

            # Configuración de la interfaz gráfica
            self.log_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD, bg="#ffffff", fg="#333333")
            self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            self.start_button = tk.Button(self.root, text="Iniciar Servidor", command=self.start_server, bg="#3498db", fg="white")
            self.start_button.pack(pady=10)

            self.HOST = '127.0.0.1'
            self.PORT = 12345
            self.server = None
            self.clients = []
            self.nicknames = []
            self.running = False

        def start_server(self):
            if self.running:
                messagebox.showinfo("Servidor", "El servidor ya está en ejecución.")
                return

            self.running = True
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.server.bind((self.HOST, self.PORT))
                self.server.listen()
                self.log_message("Servidor escuchando en {}:{}".format(self.HOST, self.PORT))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo iniciar el servidor: {e}")
                self.running = False
                return

            threading.Thread(target=self.accept_connections, daemon=True).start()
            self.start_button.config(state='disabled')

        def accept_connections(self):
            while self.running:
                try:
                    client, address = self.server.accept()
                    self.log_message(f"Conexión establecida con {str(address)}")

                    client.send('NombreCliente'.encode('utf-8'))
                    nickname = client.recv(1024).decode('utf-8')
                    self.nicknames.append(nickname)
                    self.clients.append(client)

                    self.log_message(f"El apodo del cliente es {nickname}")
                    self.broadcast(f'{nickname} se ha unido al chat!'.encode('utf-8'))
                    client.send('Conectado al servidor!'.encode('utf-8'))

                    threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
                except Exception as e:
                    self.log_message(f"Error al aceptar conexión: {e}")
                    break

        def handle_client(self, client):
            while self.running:
                try:
                    message = client.recv(1024)
                    self.broadcast(message)
                    self.log_message(message.decode('utf-8'))
                except:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[index]
                    self.broadcast(f'{nickname} salió del chat.'.encode('utf-8'))
                    self.log_message(f'{nickname} salió del chat.')
                    self.nicknames.remove(nickname)
                    break

        def broadcast(self, message):
            for client in self.clients:
                try:
                    client.send(message)
                except Exception as e:
                    self.log_message(f"Error al enviar mensaje: {e}")

        def log_message(self, message):
            self.log_area.config(state='normal')
            self.log_area.insert(tk.END, f"{message}\n")
            self.log_area.yview(tk.END)
            self.log_area.config(state='disabled')

        def stop_server(self):
            if self.running:
                self.running = False
                for client in self.clients:
                    client.close()
                self.server.close()
                self.log_message("Servidor detenido.")
                self.start_button.config(state='normal')

    class ChatClient:
        def __init__(self, root):
            self.root = root
            self.root.title("Cliente de Chat")
            self.root.configure(bg="#34495e")  # Fondo oscuro para la ventana principal

            # Configuración del socket
            self.HOST = '127.0.0.1'
            self.PORT = 12345
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Configuración de la interfaz gráfica
            self.nickname_label = tk.Label(self.root, text="Introduce tu apodo:", bg="#34495e", fg="#ffffff")
            self.nickname_label.pack(padx=10, pady=5)

            self.nickname_entry = tk.Entry(self.root)
            self.nickname_entry.pack(padx=10, pady=5)
            self.nickname_entry.bind("<Return>", self.set_nickname)

            self.connect_button = tk.Button(self.root, text="Conectar", command=self.set_nickname, bg="#3498db", fg="white")
            self.connect_button.pack(padx=10, pady=5)

            self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD, bg="#ffffff", fg="#333333")
            self.input_field = tk.Entry(self.root)
            self.send_button = tk.Button(self.root, text="Enviar", command=self.write_message, bg="#3498db", fg="white")

        def set_nickname(self, event=None):
            self.nickname = self.nickname_entry.get().strip()
            if not self.nickname:
                messagebox.showwarning("Advertencia", "El apodo no puede estar vacío.")
                return

            self.nickname_label.pack_forget()
            self.nickname_entry.pack_forget()
            self.connect_button.pack_forget()

            self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            self.input_field.pack(padx=10, pady=10, fill=tk.X)
            self.input_field.bind("<Return>", self.write_message)
            self.send_button.pack(padx=10, pady=5)

            self.connect_to_server()

        def connect_to_server(self):
            try:
                self.client.connect((self.HOST, self.PORT))
            except Exception as e:
                messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")
                self.root.destroy()
                return

            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.client.send(self.nickname.encode('ascii'))

        def receive_messages(self):
            while True:
                try:
                    message = self.client.recv(1024).decode('ascii')
                    if message == 'NombreCliente':
                        self.client.send(self.nickname.encode('ascii'))
                    else:
                        self.update_chat_area(message)
                except Exception:
                    self.update_chat_area("Ocurrió un error y se cerró la conexión.")
                    self.client.close()
                    break

        def write_message(self, event=None):
            message = self.input_field.get()
            if message.strip():
                full_message = f"{self.nickname}: {message}"
                self.client.send(full_message.encode('ascii'))
            self.input_field.delete(0, tk.END)

        def update_chat_area(self, message, from_self=False):
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"{message}\n", ("self_message" if from_self else ""))
            self.chat_area.tag_config("self_message", foreground="blue")
            self.chat_area.yview(tk.END)
            self.chat_area.config(state='disabled')

    def main():
        server_thread = threading.Thread(target=start_server_window, daemon=True)
        client_thread1 = threading.Thread(target=start_client_window, daemon=True)
        client_thread2 = threading.Thread(target=start_client_window, daemon=True)
        client_thread3 = threading.Thread(target=start_client_window, daemon=True)

        server_thread.start()
        client_thread1.start()
        client_thread2.start()
        client_thread3.start()

        server_thread.join()
        client_thread1.join()
        client_thread2.join()
        client_thread3.join()

    def start_server_window():
        server_root = tk.Tk()
        ChatServer(server_root)
        server_root.mainloop()

    def start_client_window():
        client_root = tk.Tk()
        ChatClient(client_root)
        client_root.mainloop()

    main()

if __name__ == "__main__":
    ejecutar()

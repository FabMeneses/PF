import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import simpledialog

def ejecutar():
    class ChatServer:
        def __init__(self, root):
            self.root = root
            self.root.title("Servidor de Chat")

            # Interfaz gráfica
            self.log_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
            self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            self.start_button = tk.Button(self.root, text="Iniciar Servidor", command=self.start_server)
            self.start_button.pack(pady=10)

            self.HOST = simpledialog.askstring("IP del Servidor", "RECUERDA DESACTIVAR LOS FIREWALLS\nIntroduce la IP del servidor:", parent=self.root)
            if not self.HOST:
                self.root.destroy()
                return
            self.PORT = 12345  # Cambiar al puerto deseado
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

            # Iniciar el hilo para aceptar conexiones
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

    # Crear ventana principal de Tkinter
    root = tk.Tk()
    server_app = ChatServer(root)

    # Manejar cierre de ventana
    def on_close():
        if messagebox.askokcancel("Salir", "¿Quieres detener el servidor y salir?"):
            server_app.stop_server()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
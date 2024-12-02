import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
def ejecutar():
    class ChatClient:
        def __init__(self, root):
            self.root = root
            self.root.title("Cliente de Chat")
            
            # Configuración del socket
            self.HOST = '192.168.53.75'  # Cambia esto a la IP del servidor
            self.PORT = 12345  # Cambia esto al puerto del servidor
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Interfaz gráfica
            self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
            self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            self.input_field = tk.Entry(self.root)
            self.input_field.pack(padx=10, pady=10, fill=tk.X)
            self.input_field.bind("<Return>", self.write_message)

            self.nickname = simpledialog.askstring("Apodo", "Elige un apodo:", parent=self.root)
            if not self.nickname:
                self.root.destroy()
                return

            self.connect_to_server()

        def connect_to_server(self):
            try:
                self.client.connect((self.HOST, self.PORT))
            except Exception as e:
                messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")
                self.root.destroy()
                return
            
            # Iniciar hilos de comunicación
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
            # Enviar apodo al servidor
            self.client.send(self.nickname.encode('ascii'))

        def receive_messages(self):
            while True:
                try:
                    message = self.client.recv(1024).decode('ascii')
                    if message == 'NombreCliente':
                        self.client.send(self.nickname.encode('ascii'))
                    else:
                        self.update_chat_area(message)
                except Exception as e:
                    self.update_chat_area("Ocurrió un error y se cerró la conexión.")
                    self.client.close()
                    break

        def write_message(self, event=None):
            message = self.input_field.get()
            if message.strip():
                full_message = f"{self.nickname}: {message}"
                self.client.send(full_message.encode('ascii'))
                self.update_chat_area(full_message, from_self=True)
            self.input_field.delete(0, tk.END)

        def update_chat_area(self, message, from_self=False):
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"{message}\n", ("self_message" if from_self else ""))
            self.chat_area.tag_config("self_message", foreground="blue")
            self.chat_area.yview(tk.END)
            self.chat_area.config(state='disabled')

    # Crear ventana principal de Tkinter
    root = tk.Tk()
    client_app = ChatClient(root)
    root.mainloop()
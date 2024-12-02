import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from queue import Queue

# Dirección y puerto
direccion = "localhost"
puerto = 9999

# Cola para mensajes del cliente y servidor
server_queue = Queue()
client_queue = Queue()

def ejecutar():
    def iniciar_servidor():
        def servidor():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as mySocket:
                try:
                    mySocket.bind((direccion, puerto))
                    server_queue.put(f"Servidor iniciado en {direccion}:{puerto}\n")
                    server_queue.put("Esperando mensajes...\n")

                    while True:
                        data, client_addr = mySocket.recvfrom(1024)
                        msg = data.decode()
                        server_queue.put(f"Mensaje recibido de {client_addr}: {msg}\n")

                        msg_out = f"Mensaje recibido: {msg}. Gracias."
                        mySocket.sendto(msg_out.encode(), client_addr)
                        server_queue.put(f"Enviando acuse de recibo a {client_addr}: {msg_out}\n")
                except Exception as e:
                    server_queue.put(f"Error en el servidor: {e}\n")

        threading.Thread(target=servidor, daemon=True).start()

    def iniciar_cliente():
        def cliente():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as mySocket:
                try:
                    msg = "Hola, soy un cliente UDP creado por Equipo 4."
                    client_queue.put(f"Enviando mensaje al servidor: {msg}\n")
                    mySocket.sendto(msg.encode(), (direccion, puerto))

                    data, server_addr = mySocket.recvfrom(1024)
                    msg_in = data.decode()
                    client_queue.put(f"Acuse de recibo del servidor: {msg_in}\n")
                except Exception as e:
                    client_queue.put(f"Error en el cliente: {e}\n")

        threading.Thread(target=cliente, daemon=True).start()

    def procesar_server_queue():
        while not server_queue.empty():
            msg = server_queue.get()
            server_output.insert(tk.END, msg)
            server_output.see(tk.END)
        server_root.after(100, procesar_server_queue)

    def procesar_client_queue():
        while not client_queue.empty():
            msg = client_queue.get()
            client_output.insert(tk.END, msg)
            client_output.see(tk.END)
        client_root.after(100, procesar_client_queue)

    # Ventana para el servidor
    server_root = tk.Tk()
    server_root.title("Servidor UDP")
    server_root.configure(bg="#34495e")

    server_output = scrolledtext.ScrolledText(
        server_root, wrap=tk.WORD, width=60, height=20, bg="#ffffff", fg="#000000"
    )
    server_output.pack(pady=20)

    server_button = tk.Button(
        server_root,
        text="Iniciar Servidor",
        bg="#3498db",
        fg="#ffffff",
        activebackground="#2c3e50",
        activeforeground="#ffffff",
        relief="flat",
        padx=10,
        pady=5,
    )
    server_button.configure(command=iniciar_servidor)
    server_button.pack(pady=10)

    # Ventana para el cliente
    client_root = tk.Tk()
    client_root.title("Cliente UDP")
    client_root.configure(bg="#34495e")

    client_output = scrolledtext.ScrolledText(
        client_root, wrap=tk.WORD, width=60, height=20, bg="#ffffff", fg="#000000"
    )
    client_output.pack(pady=20)

    client_button = tk.Button(
        client_root,
        text="Iniciar Cliente",
        bg="#3498db",
        fg="#ffffff",
        activebackground="#2c3e50",
        activeforeground="#ffffff",
        relief="flat",
        padx=10,
        pady=5,
    )
    client_button.configure(command=iniciar_cliente)
    client_button.pack(pady=10)

    # Procesar colas periódicamente
    server_root.after(100, procesar_server_queue)
    client_root.after(100, procesar_client_queue)

    # Ejecutar ambas ventanas
    threading.Thread(target=server_root.mainloop).start()
    client_root.mainloop()

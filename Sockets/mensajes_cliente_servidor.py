import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

direccion = "127.0.0.1"
puerto = 65432

def ejecutar():
    def servidor(output):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((direccion, puerto))
            s.listen()
            output.insert(tk.END, "Servidor: Esperando conexión del cliente...\n")
            conn, addr = s.accept()
            with conn:
                output.insert(tk.END, f"Servidor: Conectado por {addr}\n")
                while True:
                    data = conn.recv(1024)
                    if not data or data == b'fin':
                        break
                    output.insert(tk.END, f"Servidor recibe: {data.decode()}\n")
                    conn.sendall(b"Mensaje recibido")
        output.insert(tk.END, "Servidor: Conexión cerrada.\n")

    def cliente(output):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            time.sleep(3)  # Esperar al servidor
            s.connect((direccion, puerto))
            for i in range(5):
                mensaje = f"Mensaje {i}"
                output.insert(tk.END, f"Cliente envía: {mensaje}\n")
                s.sendall(mensaje.encode())
                data = s.recv(1024)
                output.insert(tk.END, f"Cliente recibe: {data.decode()}\n")
                time.sleep(1)
            s.sendall(b'fin')
        output.insert(tk.END, "Cliente: Conexión cerrada.\n")

    def iniciar_hilos():
        output.delete(1.0, tk.END)
        hilo_servidor = threading.Thread(target=servidor, args=(output,))
        hilo_cliente = threading.Thread(target=cliente, args=(output,))

        hilo_servidor.start()
        hilo_cliente.start()

    # Configuración de la interfaz gráfica
    root = tk.Tk()
    root.title("Cliente-Servidor")

    # Configuración de colores
    root.configure(bg='lightblue')
    output = scrolledtext.ScrolledText(root, width=50, height=20, bg='white', fg='black')
    output.pack(pady=10)

    btn_iniciar = tk.Button(root, text="Iniciar", command=iniciar_hilos, bg='green', fg='white')
    btn_iniciar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    ejecutar()
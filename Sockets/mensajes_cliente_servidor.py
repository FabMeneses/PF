import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
from queue import Queue

direccion = "127.0.0.1"
puerto = 65432

def ejecutar():
    def servidor(output_queue):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((direccion, puerto))
            except OSError as e:
                output_queue.put(f"Error al iniciar el servidor: {e}\n")
                return
            s.listen()
            output_queue.put("Servidor: Esperando conexión del cliente...\n")
            conn, addr = s.accept()
            with conn:
                output_queue.put(f"Servidor: Conectado por {addr}\n")
                while True:
                    data = conn.recv(1024)
                    if not data or data == b'fin':
                        break
                    output_queue.put(f"Servidor recibe: {data.decode()}\n")
                    conn.sendall(b"Mensaje recibido")
        output_queue.put("Servidor: Conexión cerrada.\n")

    def cliente(output_queue):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            time.sleep(3)  # Esperar al servidor
            try:
                s.connect((direccion, puerto))
            except ConnectionResetError as e:
                output_queue.put(f"Error al conectar con el servidor: {e}\n")
                return
            for i in range(5):
                mensaje = f"Mensaje {i}"
                output_queue.put(f"Cliente envía: {mensaje}\n")
                s.sendall(mensaje.encode())
                try:
                    data = s.recv(1024)
                except ConnectionResetError as e:
                    output_queue.put(f"Error al recibir del servidor: {e}\n")
                    break
                output_queue.put(f"Cliente recibe: {data.decode()}\n")
                time.sleep(1)
            s.sendall(b'fin')
        output_queue.put("Cliente: Conexión cerrada.\n")

    def iniciar_hilos(output_servidor, output_cliente):
        output_servidor.delete(1.0, tk.END)
        output_cliente.delete(1.0, tk.END)
        output_queue_servidor = Queue()
        output_queue_cliente = Queue()
        
        hilo_servidor = threading.Thread(target=servidor, args=(output_queue_servidor,))
        hilo_cliente = threading.Thread(target=cliente, args=(output_queue_cliente,))

        hilo_servidor.start()
        hilo_cliente.start()

        def actualizar_output(output, queue):
            while not queue.empty():
                output.insert(tk.END, queue.get())
            output.after(100, actualizar_output, output, queue)

        actualizar_output(output_servidor, output_queue_servidor)
        actualizar_output(output_cliente, output_queue_cliente)

    def crear_ventana(titulo, iniciar_funcion):
        ventana = tk.Tk()
        ventana.title(titulo)
        ventana.configure(bg='#34495e')
        output = scrolledtext.ScrolledText(ventana, width=50, height=20, bg='white', fg='black')
        output.pack(pady=10)
        btn_iniciar = tk.Button(ventana, text="Iniciar", command=lambda: iniciar_funcion(output), bg='#3498db', fg='white')
        btn_iniciar.pack(pady=10)
        return ventana, output

    # Crear ventanas para servidor y cliente
    ventana_servidor, output_servidor = crear_ventana("Servidor", lambda output: iniciar_hilos(output, output_cliente))
    ventana_cliente, output_cliente = crear_ventana("Cliente", lambda output: iniciar_hilos(output_servidor, output))

    # Ejecutar las ventanas en el hilo principal
    ventana_servidor.mainloop()
    ventana_cliente.mainloop()

if __name__ == "__main__":
    ejecutar()

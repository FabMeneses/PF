import socket
import threading
import random
import time
import tkinter as tk
from tkinter import messagebox

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 65432
MAX_CONNECTIONS = 5
def ejecutar():
    global server_running, server_socket
    # Semaphore para limitar las conexiones concurrentes
    semaphore = threading.Semaphore(MAX_CONNECTIONS)

    # Variable global para controlar el servidor
    server_running = False
    server_socket = None

    # Configuración de la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Servidor Tigres")
    ventana_principal.geometry("600x500")
    ventana_principal.configure(bg="#34495e")  # Fondo gris oscuro

    # Título y frase alusiva
    etiqueta_titulo = tk.Label(
        ventana_principal, 
        text="Servidor Tigres - ¡Unidos hasta el final!", 
        font=("Arial", 16), 
        bg="#34495e",  # Fondo gris oscuro
        fg="#ffffff"  # Texto blanco
    )
    etiqueta_titulo.pack(pady=10)

    # Agregar un cuadro de texto para mostrar el log
    cuadro_log = tk.Text(ventana_principal, height=20, width=70, state="disabled", font=("Arial", 10), bg="white", fg="black")
    cuadro_log.pack(pady=10)

    # Función para agregar mensajes al cuadro de log
    def agregar_log(mensaje):
        cuadro_log.config(state="normal")
        cuadro_log.insert(tk.END, f"{mensaje}\n")
        cuadro_log.config(state="disabled")
        cuadro_log.see(tk.END)

    # Función para manejar la conexión con un cliente
    def handle_client(connection, address):
        with connection:
            agregar_log(f"Cliente conectado desde {address}")
            sleep_time = random.uniform(1, 5)
            agregar_log(f"Procesando tarea para {address}, durará {sleep_time:.2f} segundos.")
            time.sleep(sleep_time)

            # Enviar respuesta al cliente
            message = f"Tarea completada en {sleep_time:.2f} segundos.\n"
            connection.sendall(message.encode('utf-8'))
            agregar_log(f"Tarea completada para {address}. Conexión cerrada.")

    # Función principal del servidor
    def server_task():
        global server_running, server_socket
        agregar_log(f"Iniciando servidor en {HOST}:{PORT}")
        server_running = True

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((HOST, PORT))
                server_socket.listen()
                agregar_log(f"Servidor escuchando en {HOST}:{PORT}")

                while server_running:
                    try:
                        server_socket.settimeout(1.0)  # Tiempo de espera para aceptar conexiones
                        connection, address = server_socket.accept()
                        semaphore.acquire()
                        agregar_log(f"Conexión aceptada de {address}")

                        # Manejar el cliente en un hilo separado
                        thread = threading.Thread(target=handle_client, args=(connection, address))
                        thread.start()
                        thread.join()
                        semaphore.release()
                    except socket.timeout:
                        continue  # Salir del bucle si no hay conexiones y server_running es False
        except Exception as e:
            agregar_log(f"Error del servidor: {e}")
        finally:
            agregar_log("Servidor detenido.")
            server_running = False

    # Botón para iniciar el servidor
    def iniciar_servidor():
        global server_running
        if (server_running):
            agregar_log("El servidor ya está en ejecución.")
            return
        threading.Thread(target=server_task, daemon=True).start()
        agregar_log("Servidor iniciado.")

    # Botón para detener el servidor
    def detener_servidor():
        global server_running, server_socket
        if not server_running:
            agregar_log("El servidor no está en ejecución.")
            return
        server_running = False
        if server_socket:
            server_socket.close()
        agregar_log("Servidor detenido manualmente.")

    # Agregar botones de control
    boton_iniciar = tk.Button(
        ventana_principal, 
        text="Iniciar Servidor", 
        command=iniciar_servidor, 
        font=("Arial", 12), 
        bg="#3498db",  # Azul brillante
        fg="#ffffff"  # Texto blanco
    )
    boton_iniciar.pack(pady=10)

    boton_detener = tk.Button(
        ventana_principal, 
        text="Detener Servidor", 
        command=detener_servidor, 
        font=("Arial", 12), 
        bg="#3498db",  # Azul brillante
        fg="#ffffff"  # Texto blanco
    )
    boton_detener.pack(pady=5)

    # Ejecutar la ventana principal
    ventana_principal.mainloop()

import socket
import threading
import time
import random
from threading import Semaphore
import tkinter as tk
from tkinter import messagebox

# Configuración de los actores
HOST = '127.0.0.1'  # Dirección de loopback (localhost)
PORT_ACTOR1 = 5001  # Puerto para Actor1
PORT_ACTOR2 = 5002  # Puerto para Actor2

def ejecutar():
    # Contador de mensajes
    MAX_MESSAGES = 100
    message_counter = 0

    # Semáforos para controlar el acceso a los recursos compartidos
    semaphore_actor1 = Semaphore(1)
    semaphore_actor2 = Semaphore(1)

    # Estado de los hilos
    running = True

    # Función para escuchar mensajes de un puerto específico
    def listen_actor(port, actor_name, semaphore, log_widget):
        nonlocal message_counter, running
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, port))
            server_socket.listen()
            agregar_log(log_widget, f"{actor_name} escuchando en el puerto {port}")
            
            while message_counter < MAX_MESSAGES and running:
                conn, addr = server_socket.accept()
                with conn:
                    data = conn.recv(1024).decode('utf-8')
                    if data:
                        with semaphore:
                            message_counter += 1
                            agregar_log(log_widget, f"{actor_name} recibió: {data}")
                            agregar_log(log_widget, f"{actor_name} está ahora en estado: Ocupado")
                            time.sleep(1)  # Simulación de procesamiento

    # Función para enviar mensajes periódicamente a otro puerto
    def send_actor(target_port, actor_name, semaphore, log_widget):
        nonlocal message_counter, running
        while message_counter < MAX_MESSAGES and running:
            with semaphore:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    try:
                        client_socket.connect((HOST, target_port))
                        message = f"Hola desde {actor_name}"
                        client_socket.sendall(message.encode('utf-8'))
                        agregar_log(log_widget, f"{actor_name} envió: {message}")
                        time.sleep(random.uniform(0.5, 1.5))  # Espera aleatoria
                    except ConnectionRefusedError:
                        agregar_log(log_widget, f"{actor_name} no pudo conectar a {target_port}")
                        time.sleep(1)

    # Función para agregar mensajes al log en la interfaz
    def agregar_log(widget, mensaje):
        widget.config(state="normal")
        widget.insert(tk.END, f"{mensaje}\n")
        widget.config(state="disabled")
        widget.see(tk.END)

    # Función para iniciar los actores
    def iniciar_actores(log_widget):
        nonlocal running, message_counter
        running = True
        message_counter = 0

        actor1_listen_thread = threading.Thread(target=listen_actor, args=(PORT_ACTOR1, "Actor1", semaphore_actor1, log_widget))
        actor2_listen_thread = threading.Thread(target=listen_actor, args=(PORT_ACTOR2, "Actor2", semaphore_actor2, log_widget))
        actor1_send_thread = threading.Thread(target=send_actor, args=(PORT_ACTOR2, "Actor1", semaphore_actor1, log_widget))
        actor2_send_thread = threading.Thread(target=send_actor, args=(PORT_ACTOR1, "Actor2", semaphore_actor2, log_widget))

        # Iniciar hilos
        actor1_listen_thread.start()
        actor2_listen_thread.start()
        actor1_send_thread.start()
        actor2_send_thread.start()

    # Función para detener los actores
    def detener_actores():
        nonlocal running
        running = False
        # Eliminar la ventana emergente
        # messagebox.showinfo("Estado", "Actores detenidos.")

    # Configuración de la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Interacción entre Actores")
    ventana_principal.geometry("600x500")
    ventana_principal.configure(bg="#34495e")  # Fondo gris oscuro

    # Título
    etiqueta_titulo = tk.Label(
        ventana_principal, 
        text="Actores en Interacción - ¡Conectados Siempre!", 
        font=("Arial", 14), 
        bg="#34495e",  # Fondo gris oscuro
        fg="#ffffff"  # Texto blanco
    )
    etiqueta_titulo.pack(pady=10)

    # Cuadro de texto para mostrar el log
    cuadro_log = tk.Text(
        ventana_principal, 
        height=20, 
        width=70, 
        state="disabled", 
        font=("Arial", 10), 
        bg="#ffffff",  # Fondo blanco para la terminal
        fg="#000000"  # Texto negro
    )
    cuadro_log.pack(pady=10)

    # Botón para iniciar actores
    boton_iniciar = tk.Button(
        ventana_principal, 
        text="Iniciar Actores", 
        command=lambda: iniciar_actores(cuadro_log), 
        font=("Arial", 12), 
        bg="#3498db",  # Fondo azul brillante
        fg="#ffffff"  # Texto blanco
    )
    boton_iniciar.pack(pady=5)

    # Botón para detener actores
    boton_detener = tk.Button(
        ventana_principal, 
        text="Detener Actores", 
        command=detener_actores, 
        font=("Arial", 12), 
        bg="#3498db",  # Fondo azul brillante
        fg="#ffffff"  # Texto blanco
    )
    boton_detener.pack(pady=5)

    # Ejecutar la ventana principal
    ventana_principal.mainloop()

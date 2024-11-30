import socket
import tkinter as tk
from tkinter import messagebox
from threading import Thread

# Configuración del servidor al que se conectará el cliente
SERVER_HOST = '127.0.0.1'  # Dirección IP del servidor
SERVER_PORT = 65432        # Puerto del servidor
def ejecutar():
    def conectar_servidor():
        """
        Conecta al servidor, envía una solicitud y muestra la respuesta.
        """
        def tarea_conexion():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                try:
                    # Conectar al servidor
                    client_socket.connect((SERVER_HOST, SERVER_PORT))
                    agregar_log(f"Conectado al servidor {SERVER_HOST}:{SERVER_PORT}")

                    # Recibir respuesta del servidor
                    response = client_socket.recv(1024).decode('utf-8')
                    agregar_log(f"Respuesta del servidor: {response}")
                except ConnectionRefusedError:
                    agregar_log("No se pudo conectar al servidor. Asegúrate de que el servidor está ejecutándose.")

        # Ejecutar la tarea de conexión en un hilo separado
        Thread(target=tarea_conexion).start()

    # Función para agregar mensajes al log
    def agregar_log(mensaje):
        cuadro_log.config(state="normal")
        cuadro_log.insert(tk.END, f"{mensaje}\n")
        cuadro_log.config(state="disabled")
        cuadro_log.see(tk.END)

    # Configuración de la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Cliente Tigres")
    ventana_principal.geometry("600x500")
    ventana_principal.configure(bg="#34495e")  # Fondo gris oscuro

    # Título y frase alusiva
    etiqueta_titulo = tk.Label(
        ventana_principal, 
        text="Cliente Tigres - ¡Siempre al ataque!", 
        font=("Arial", 16), 
        bg="#34495e",  # Fondo gris oscuro
        fg="#ffffff"  # Texto blanco
    )
    etiqueta_titulo.pack(pady=10)

    # Cuadro de texto para el log
    cuadro_log = tk.Text(ventana_principal, height=20, width=70, state="disabled", font=("Arial", 10), bg="white", fg="black")
    cuadro_log.pack(pady=10)

    # Botón para conectar al servidor
    boton_conectar = tk.Button(
        ventana_principal, 
        text="Conectar al Servidor", 
        command=conectar_servidor, 
        font=("Arial", 12), 
        bg="#3498db",  # Azul brillante
        fg="#ffffff"  # Texto blanco
    )
    boton_conectar.pack(pady=10)

    # Ejecutar la ventana principal
    ventana_principal.mainloop()

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Diccionario de usuarios y contraseñas
users = {
    "fab1": "hola1",
    "fab2": "hola2",
    "fab3": "hola3",
    "fab4": "hola4",
    "fab5": "hola5"
}

# Dirección y puerto
direccion = 'localhost'
puerto = 12345

# Función para iniciar el servidor
def iniciar_servidor(output):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((direccion, puerto))
    server_socket.listen(5)

    output.insert(tk.END, "Servidor iniciado. Esperando cliente...\n")
    output.yview(tk.END)

    while True:
        client_socket, address = server_socket.accept()
        output.insert(tk.END, f"Conexión aceptada con {address}\n")
        output.yview(tk.END)
        
        data = client_socket.recv(1024).decode()
        username, password = data.split(',')

        if username in users and users[username] == password:
            response = "Autenticación exitosa"
        else:
            response = "Autenticación fallida"

        client_socket.send(response.encode())
        client_socket.close()

# Función para la autenticación del cliente
def authenticate(output, entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((direccion, puerto))
        client_socket.send(f"{username},{password}".encode())
        response = client_socket.recv(1024).decode()
        
        output.insert(tk.END, f"Respuesta del servidor: {response}\n")
        output.yview(tk.END)
        client_socket.close()
    except Exception as e:
        output.insert(tk.END, f"Error: {e}\n")
        output.yview(tk.END)

def iniciar_hilos(output, entry_username, entry_password):
    hilo_servidor = threading.Thread(target=iniciar_servidor, args=(output,))
    hilo_servidor.daemon = True
    hilo_servidor.start()

    hilo_cliente = threading.Thread(target=authenticate, args=(output, entry_username, entry_password))
    hilo_cliente.start()

def ejecutar():
    root = tk.Tk()
    root.title("Autenticación Águila")
    root.configure(bg="#34495e")  # Fondo gris oscuro

    # Área de texto para mostrar los mensajes
    output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, bg="#ffffff", fg="#1C2833")  # Fondo blanco para la terminal
    output.pack(pady=20)

    # Campos de entrada para el nombre de usuario y la contraseña
    tk.Label(root, text="Nombre de usuario:", bg="#34495e", fg="#ffffff").pack()  # Texto blanco
    entry_username = tk.Entry(root, bg="#D5DBDB", fg="#1C2833")
    entry_username.pack()

    tk.Label(root, text="Contraseña:", bg="#34495e", fg="#ffffff").pack()  # Texto blanco
    entry_password = tk.Entry(root, show="*", bg="#D5DBDB", fg="#1C2833")
    entry_password.pack()

    # Botón para iniciar la autenticación
    start_button = tk.Button(root, text="Iniciar Autenticación", command=lambda: iniciar_hilos(output, entry_username, entry_password), bg="#3498db", fg="#ffffff")  # Botón azul brillante con texto blanco
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    ejecutar()
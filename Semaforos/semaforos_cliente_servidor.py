import socket
import threading
from threading import Semaphore
import tkinter as tk

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 65432
MAX_CLIENTES_SIMULTANEOS = 3

semaforo = Semaphore(MAX_CLIENTES_SIMULTANEOS)

def actualizar_mensaje(mensaje, text_widget):
    text_widget.insert(tk.END, mensaje + "\n")
    text_widget.yview(tk.END)

def manejar_cliente(conexion, direccion, text_widget):
    with semaforo:
        mensaje = conexion.recv(1024).decode('utf-8')
        respuesta = "Mensaje recibido y confirmado"
        
        actualizar_mensaje(f"Cliente ({direccion}): {mensaje}", text_widget)
        conexion.sendall(respuesta.encode('utf-8'))
        actualizar_mensaje(f"Servidor: {respuesta}", text_widget)

        conexion.close()

def iniciar_servidor(text_widget):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PORT))
        servidor.listen(5)
        actualizar_mensaje(f"Servidor escuchando en {HOST}:{PORT}", text_widget)

        while True:
            conexion, direccion = servidor.accept()
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion, text_widget))
            hilo_cliente.start()

def iniciar_cliente(text_widget):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        mensaje = "Hola, servidor"
        cliente.sendall(mensaje.encode('utf-8'))

        respuesta = cliente.recv(1024).decode('utf-8')
        
        actualizar_mensaje(f"Cliente: {mensaje}", text_widget)
        actualizar_mensaje(f"Servidor: {respuesta}", text_widget)

def ejecutar():
    def iniciar_servidor_en_hilo(text_widget):
        servidor_thread = threading.Thread(target=iniciar_servidor, args=(text_widget,))
        servidor_thread.daemon = True
        servidor_thread.start()

    def iniciar_cliente_en_hilo(text_widget):
        cliente_thread = threading.Thread(target=iniciar_cliente, args=(text_widget,))
        cliente_thread.daemon = True
        cliente_thread.start()

    def crear_ventana_servidor():
        ventana_servidor = tk.Tk()
        ventana_servidor.title("Servidor")
        ventana_servidor.configure(bg='lightblue')

        text_widget_servidor = tk.Text(ventana_servidor, height=20, width=80, wrap=tk.WORD, bg='white', fg='black')
        text_widget_servidor.pack(padx=10, pady=10)

        tk.Button(ventana_servidor, text="Iniciar Servidor", command=lambda: iniciar_servidor_en_hilo(text_widget_servidor), width=20, height=2, bg='green', fg='white').pack(pady=5)

        ventana_servidor.mainloop()

    def crear_ventana_cliente():
        ventana_cliente = tk.Tk()
        ventana_cliente.title("Cliente")
        ventana_cliente.configure(bg='lightgreen')

        text_widget_cliente = tk.Text(ventana_cliente, height=20, width=80, wrap=tk.WORD, bg='white', fg='black')
        text_widget_cliente.pack(padx=10, pady=10)

        tk.Button(ventana_cliente, text="Iniciar Cliente", command=lambda: iniciar_cliente_en_hilo(text_widget_cliente), width=20, height=2, bg='blue', fg='white').pack(pady=5)

        ventana_cliente.mainloop()

    hilo_ventana_servidor = threading.Thread(target=crear_ventana_servidor)
    hilo_ventana_servidor.daemon = True
    hilo_ventana_servidor.start()

    hilo_ventana_cliente = threading.Thread(target=crear_ventana_cliente)
    hilo_ventana_cliente.daemon = True
    hilo_ventana_cliente.start()

    tk.mainloop()

import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

direccion = '127.0.0.1'
puerto_udp = 9999
puerto_tcp = 10000

def servidor_udp(output):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.bind((direccion, puerto_udp))
    output.insert(tk.END, f"Servidor UDP enlazado a la dirección {direccion} y puerto {puerto_udp}\n")
    output.yview(tk.END)
    
    while True:
        msg, client_addr = mySocket.recvfrom(1024)
        output.insert(tk.END, f"Mensaje recibido del cliente UDP: {msg.decode()}\n")
        output.insert(tk.END, "Enviando acuse de recibido al cliente.\n")
        msg_out = f"Mensaje recibido: {msg.decode()}, Gracias.".encode()
        mySocket.sendto(msg_out, client_addr)
        output.yview(tk.END)

def cliente_udp(output):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(5):
        msg = f"Mensaje UDP {i}"
        output.insert(tk.END, f"Cliente UDP envía: {msg}\n")
        mySocket.sendto(msg.encode(), (direccion, puerto_udp))
        data, _ = mySocket.recvfrom(1024)
        output.insert(tk.END, f"Cliente UDP recibe: {data.decode()}\n")
        output.yview(tk.END)
        time.sleep(1)
    mySocket.sendto(b'fin', (direccion, puerto_udp))
    output.insert(tk.END, "Cliente UDP: Conexión cerrada.\n")

def servidor_tcp(output):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind((direccion, puerto_tcp))
    mySocket.listen(1)
    output.insert(tk.END, f"Servidor TCP enlazado a la dirección {direccion} y puerto {puerto_tcp}\n")
    output.yview(tk.END)
    
    conn, addr = mySocket.accept()
    with conn:
        output.insert(tk.END, f"Conexión TCP establecida con {addr}\n")
        while True:
            msg = conn.recv(1024)
            if not msg or msg == b'fin':
                break
            output.insert(tk.END, f"Mensaje recibido del cliente TCP: {msg.decode()}\n")
            output.insert(tk.END, "Enviando acuse de recibido al cliente.\n")
            msg_out = f"Mensaje recibido: {msg.decode()}, Gracias.".encode()
            conn.sendall(msg_out)
            output.yview(tk.END)
    output.insert(tk.END, "Servidor TCP: Conexión cerrada.\n")

def cliente_tcp(output):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(3)  # Esperar al servidor
    mySocket.connect((direccion, puerto_tcp))
    for i in range(5):
        msg = f"Mensaje TCP {i}"
        output.insert(tk.END, f"Cliente TCP envía: {msg}\n")
        mySocket.sendall(msg.encode())
        data = mySocket.recv(1024)
        output.insert(tk.END, f"Cliente TCP recibe: {data.decode()}\n")
        output.yview(tk.END)
        time.sleep(1)
    mySocket.sendall(b'fin')
    output.insert(tk.END, "Cliente TCP: Conexión cerrada.\n")

def iniciar_hilos(output):
    hilo_servidor_udp = threading.Thread(target=servidor_udp, args=(output,))
    hilo_cliente_udp = threading.Thread(target=cliente_udp, args=(output,))
    hilo_servidor_tcp = threading.Thread(target=servidor_tcp, args=(output,))
    hilo_cliente_tcp = threading.Thread(target=cliente_tcp, args=(output,))

    hilo_servidor_udp.start()
    hilo_cliente_udp.start()
    hilo_servidor_tcp.start()
    hilo_cliente_tcp.start()

def ejecutar():
    root = tk.Tk()
    root.title("Comunicación Directa UDP y TCP")
    root.configure(bg='#34495e')  # Fondo gris oscuro

    output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, bg='#ffffff', fg='#000000')  # Fondo blanco para la terminal
    output.pack(pady=20)

    start_button = tk.Button(root, text="Iniciar Comunicación", command=lambda: iniciar_hilos(output), bg='#3498db', fg='#ffffff')  # Botón azul brillante con texto blanco
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    ejecutar()
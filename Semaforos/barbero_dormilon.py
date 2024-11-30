import threading
import time
import random
import tkinter as tk

NUMERO_SILLAS = 3
COLORES_CLIENTES = ["#0000FF", "#FF0000", "#008000", "#000000", "#FFA500", "#800080", "#00FFFF", "#FFC0CB"]

class Barberia:
    def __init__(self, text_widget):
        self.sillas_sala_espera = NUMERO_SILLAS
        self.sillas_sem = threading.Semaphore(NUMERO_SILLAS)
        self.barbero_dormido = threading.Semaphore(0)
        self.silla_barbero = threading.Lock()
        self.corte_realizado = threading.Semaphore(0)
        self.text_widget = text_widget
        self.clientes_atendidos = 0

    def actualizar_mensaje(self, mensaje, color="#000000"):
        self.text_widget.after(0, self._insertar_mensaje, mensaje, color)

    def _insertar_mensaje(self, mensaje, color):
        self.text_widget.insert(tk.END, mensaje + "\n", ("color",))
        self.text_widget.tag_configure("color", foreground=color)
        self.text_widget.yview(tk.END)

    def cortar_pelo(self, cliente_id, color):
        mensaje = f"El barbero está cortando el pelo del cliente {cliente_id}."
        self.actualizar_mensaje(mensaje, color)
        time.sleep(random.uniform(1, 3))
        mensaje = f"El barbero ha terminado de cortar el pelo del cliente {cliente_id}."
        self.actualizar_mensaje(mensaje, color)

def cliente(barberia, cliente_id, color):
    mensaje = f"El cliente {cliente_id} ha llegado."
    barberia.actualizar_mensaje(mensaje, color)
    
    if barberia.sillas_sem.acquire(blocking=False):
        mensaje = f"El cliente {cliente_id} está esperando en la sala de espera."
        barberia.actualizar_mensaje(mensaje, color)
        
        with barberia.silla_barbero:
            barberia.sillas_sem.release()
            mensaje = f"El cliente {cliente_id} está siendo atendido."
            barberia.actualizar_mensaje(mensaje, color)
            barberia.barbero_dormido.release()
            barberia.corte_realizado.acquire()
            mensaje = f"El cliente {cliente_id} se va con el pelo cortado."
            barberia.actualizar_mensaje(mensaje, color)
    else:
        mensaje = f"El cliente {cliente_id} se va porque la sala de espera está llena."
        barberia.actualizar_mensaje(mensaje, color)

def barbero(barberia):
    while True:
        mensaje = "El barbero está durmiendo."
        barberia.actualizar_mensaje(mensaje)
        barberia.barbero_dormido.acquire()
        mensaje = "El barbero ha sido despertado."
        barberia.actualizar_mensaje(mensaje)

        barberia.cortar_pelo(barberia.clientes_atendidos + 1, COLORES_CLIENTES[barberia.clientes_atendidos % len(COLORES_CLIENTES)])
        barberia.corte_realizado.release()

        barberia.clientes_atendidos += 1
        if barberia.clientes_atendidos >= 10:
            break

def ejecutar():
    ventana_barberia = tk.Tk()
    ventana_barberia.title("Barbero Dormilón")
    ventana_barberia.configure(bg="#34495e")  # Fondo gris oscuro

    text_widget = tk.Text(ventana_barberia, height=20, width=80, wrap=tk.WORD, bg="#ffffff", fg="#ffffff")  # Texto blanco
    text_widget.pack(padx=10, pady=10)

    tk.Button(ventana_barberia, text="Iniciar Barbería", command=lambda: iniciar_barberia(text_widget), width=20, height=2, bg="#3498db", fg="#ffffff").pack(pady=5)  # Botón azul brillante con texto blanco

    ventana_barberia.mainloop()

def iniciar_barberia(text_widget):
    barberia = Barberia(text_widget)
    
    hilo_barbero = threading.Thread(target=barbero, args=(barberia,))
    hilo_barbero.daemon = True
    hilo_barbero.start()

    def crear_cliente(cliente_id):
        color = COLORES_CLIENTES[(cliente_id - 1) % len(COLORES_CLIENTES)]
        hilo_cliente = threading.Thread(target=cliente, args=(barberia, cliente_id, color))
        hilo_cliente.daemon = True
        hilo_cliente.start()

        if cliente_id < 10:
            text_widget.after(random.randint(2000, 5000), crear_cliente, cliente_id + 1)

    crear_cliente(1)

import threading
import time
import random
import tkinter as tk

NUMERO_SILLAS = 3
COLORES_CLIENTES = ["#0000FF", "#FF0000", "#008000", "#000000", "#FFA500", "#800080", "#00FFFF", "#FFC0CB"]

class Barberia:
    def __init__(self, text_widget_barbero, text_widget_cliente):
        self.sillas_sala_espera = NUMERO_SILLAS
        self.sillas_sem = threading.Semaphore(NUMERO_SILLAS)
        self.barbero_dormido = threading.Semaphore(0)
        self.silla_barbero = threading.Lock()
        self.corte_realizado = threading.Semaphore(0)
        self.text_widget_barbero = text_widget_barbero
        self.text_widget_cliente = text_widget_cliente
        self.clientes_atendidos = 0

    def actualizar_mensaje(self, mensaje, color="#000000", es_barbero=True):
        widget = self.text_widget_barbero if es_barbero else self.text_widget_cliente
        if widget.winfo_exists() and widget.winfo_ismapped():
            widget.after(0, self._insertar_mensaje, widget, mensaje, color)

    def _insertar_mensaje(self, widget, mensaje, color):
        if widget.winfo_exists() and widget.winfo_ismapped():
            widget.insert(tk.END, mensaje + "\n", ("color",))
            widget.tag_configure("color", foreground=color)
            widget.yview(tk.END)

    def cortar_pelo(self, cliente_id, color):
        mensaje = f"El barbero está cortando el pelo del cliente {cliente_id}."
        self.actualizar_mensaje(mensaje, color, es_barbero=True)
        time.sleep(random.uniform(1, 3))
        mensaje = f"El barbero ha terminado de cortar el pelo del cliente {cliente_id}."
        self.actualizar_mensaje(mensaje, color, es_barbero=True)

def cliente(barberia, cliente_id, color):
    mensaje = f"El cliente {cliente_id} ha llegado."
    barberia.actualizar_mensaje(mensaje, color, es_barbero=False)
    
    if barberia.sillas_sem.acquire(blocking=False):
        mensaje = f"El cliente {cliente_id} está esperando en la sala de espera."
        barberia.actualizar_mensaje(mensaje, color, es_barbero=False)
        
        with barberia.silla_barbero:
            barberia.sillas_sem.release()
            mensaje = f"El cliente {cliente_id} está siendo atendido."
            barberia.actualizar_mensaje(mensaje, color, es_barbero=False)
            barberia.barbero_dormido.release()
            barberia.corte_realizado.acquire()
            mensaje = f"El cliente {cliente_id} se va con el pelo cortado."
            barberia.actualizar_mensaje(mensaje, color, es_barbero=False)
    else:
        mensaje = f"El cliente {cliente_id} se va porque la sala de espera está llena."
        barberia.actualizar_mensaje(mensaje, color, es_barbero=False)

def barbero(barberia):
    while True:
        mensaje = "El barbero está durmiendo."
        barberia.actualizar_mensaje(mensaje, es_barbero=True)
        barberia.barbero_dormido.acquire()
        mensaje = "El barbero ha sido despertado."
        barberia.actualizar_mensaje(mensaje, es_barbero=True)

        barberia.cortar_pelo(barberia.clientes_atendidos + 1, COLORES_CLIENTES[barberia.clientes_atendidos % len(COLORES_CLIENTES)])
        barberia.corte_realizado.release()

        barberia.clientes_atendidos += 1

def ejecutar():
    ventana_barbero = tk.Tk()
    ventana_barbero.title("Barbero Dormilón - Barbero")
    ventana_barbero.configure(bg="#34495e")  # Fondo gris oscuro

    text_widget_barbero = tk.Text(ventana_barbero, height=20, width=80, wrap=tk.WORD, bg="#ffffff", fg="#000000")
    text_widget_barbero.pack(padx=10, pady=10)

    ventana_cliente = tk.Toplevel(ventana_barbero)
    ventana_cliente.title("Barbero Dormilón - Cliente")
    ventana_cliente.configure(bg="#34495e")  # Fondo gris oscuro

    text_widget_cliente = tk.Text(ventana_cliente, height=20, width=80, wrap=tk.WORD, bg="#ffffff", fg="#000000")
    text_widget_cliente.pack(padx=10, pady=10)

    tk.Button(ventana_barbero, text="Iniciar Barbería", command=lambda: iniciar_barbero(text_widget_barbero, text_widget_cliente), width=20, height=2, bg="#3498db", fg="#ffffff").pack(pady=5)  # Botón azul brillante con texto blanco
    tk.Button(ventana_cliente, text="Iniciar Cliente", command=lambda: iniciar_cliente(text_widget_cliente), width=20, height=2, bg="#3498db", fg="#ffffff").pack(pady=5)  # Botón azul brillante con texto blanco

    ventana_barbero.mainloop()

def iniciar_barbero(text_widget_barbero, text_widget_cliente):
    global barberia
    barberia = Barberia(text_widget_barbero, text_widget_cliente)
    
    hilo_barbero = threading.Thread(target=barbero, args=(barberia,))
    hilo_barbero.daemon = True
    hilo_barbero.start()

def iniciar_cliente(text_widget_cliente):
    def crear_cliente(cliente_id):
        color = COLORES_CLIENTES[(cliente_id - 1) % len(COLORES_CLIENTES)]
        text_widget_cliente.after(0, lambda: threading.Thread(target=cliente, args=(barberia, cliente_id, color)).start())
        text_widget_cliente.after(random.randint(1000, 2000), crear_cliente, cliente_id + 1)

    crear_cliente(1)

if __name__ == "__main__":
    ejecutar()
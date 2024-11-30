import threading
import time
import tkinter as tk
from tkinter import ttk

def tarea_que_toma_tiempo(nombre, label):
    label.config(text=f"Inicio de la tarea {nombre}")
    time.sleep(2)
    label.config(text=f"Fin de la tarea {nombre}")
    if nombre == "Hilo 1":
        hilo1_terminado.set(True)
    elif nombre == "Hilo 2":
        hilo2_terminado.set(True)
    if hilo1_terminado.get() and hilo2_terminado.get():
        label_status.config(text="Todos los hilos han terminado.")

def iniciar_hilos():
    hilo1_terminado.set(False)
    hilo2_terminado.set(False)
    hilo1 = threading.Thread(target=tarea_que_toma_tiempo, args=("Hilo 1", label1))
    hilo2 = threading.Thread(target=tarea_que_toma_tiempo, args=("Hilo 2", label2))
    hilo1.start()
    hilo2.start()

def ejecutar():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Ejemplo de Hilos con Tkinter")
    root.geometry("400x150")
    root.configure(bg="#34495e")  # Fondo gris oscuro

    # Variables para controlar el estado de los hilos
    global hilo1_terminado, hilo2_terminado, label1, label2, label_status
    hilo1_terminado = tk.BooleanVar(value=False)
    hilo2_terminado = tk.BooleanVar(value=False)

    # Crear etiquetas para mostrar el estado de los hilos
    label1 = ttk.Label(root, text="Esperando para iniciar Hilo 1", foreground="white", background="#34495e")
    label1.pack(pady=10)
    label2 = ttk.Label(root, text="Esperando para iniciar Hilo 2", foreground="white", background="#34495e")
    label2.pack(pady=10)

    # Crear un botón para iniciar los hilos
    style = ttk.Style()
    style.configure("TButton", background="#3498db", foreground="black", borderwidth=1, focusthickness=3, focuscolor='none')
    style.map("TButton", background=[('active', '#2980b9')])

    boton_iniciar = ttk.Button(root, text="Iniciar Hilos", command=iniciar_hilos, style="TButton")
    boton_iniciar.pack(pady=20)

    # Crear una etiqueta para mostrar el estado general
    label_status = ttk.Label(root, text="", foreground="white", background="#34495e")
    label_status.pack(pady=10)

    # Iniciar el bucle principal de la interfaz
    root.mainloop()

if __name__ == "__main__":
    ejecutar()
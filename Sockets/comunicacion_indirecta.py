import threading
import queue
import time
import random
import tkinter as tk
from tkinter import scrolledtext

# Generar una lista de números aleatorios
n = [random.randint(1, 101) for i in range(101)]

# Cola de comunicación entre hilos
cola = queue.Queue()

def ejecutar():
    # Función del productor
    def productor(output):
        for i in n:
            item = f"Mensaje {i}"
            output.insert(tk.END, f"Productor: {item}\n")
            output.yview(tk.END)  # Hacer scroll automáticamente hacia abajo
            cola.put(i)
            time.sleep(1)
        cola.put(None)  # Señal de terminación

    # Función del consumidor
    def consumidor(output):
        while True:
            item = cola.get()
            if item is None:
                break  # Salir del bucle si se recibe la señal de terminación
            output.insert(tk.END, f"Consumidor: Mensaje {item}\n")
            output.yview(tk.END)  # Hacer scroll automáticamente hacia abajo
            time.sleep(1)

    # Configuración de la interfaz gráfica
    root = tk.Tk()
    root.title("Comunicación Indirecta con Sockets")

    # Configuración de colores
    root.configure(bg='#2e3f4f')
    output = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg='#1c2833', fg='#f7f9f9', insertbackground='white')
    output.pack(padx=10, pady=10)

    # Crear y arrancar los hilos
    hilo_productor = threading.Thread(target=productor, args=(output,))
    hilo_consumidor = threading.Thread(target=consumidor, args=(output,))

    hilo_productor.start()
    hilo_consumidor.start()

    root.mainloop()

if __name__ == "__main__":
    ejecutar()
import threading
import tkinter as tk
from tkinter import messagebox

# Función que se ejecutará en el hilo
def Primer_Hilo(label):
    # Actualizar el texto en el widget de la etiqueta
    label.config(text="Mi Primer Programa con Hilos en Python")

# Función principal para ejecutar este módulo
def ejecutar():
    # Crear la ventana principal de tkinter
    root = tk.Tk()
    root.title("Hilos-Hilos")
    root.geometry("400x150")
    root.configure(bg="#34495e")  # Fondo gris oscuro

    # Crear y empaquetar una etiqueta en la ventana
    label = tk.Label(root, text="Esperando ejecución del hilo...", fg="#ffffff", bg="#34495e")
    label.pack(pady=20)

    # Función para iniciar el hilo
    def iniciar_hilo():
        thread = threading.Thread(target=Primer_Hilo, args=(label,))
        thread.start()

    # Crear y empaquetar un botón en la ventana
    boton = tk.Button(root, text="Iniciar Hilo", command=iniciar_hilo, bg="#3498db", fg="#ffffff", activebackground="#2980b9", activeforeground="#ffffff")
    boton.pack(pady=10)

    # Iniciar el bucle principal de tkinter
    root.mainloop()

# Ejecutar la función principal
if __name__ == "__main__":
    ejecutar()

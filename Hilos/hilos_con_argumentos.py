import threading
import time
import tkinter as tk

def ejecutar():
    def Hilo_02(nombre, apellido, label):
        # Actualiza la etiqueta con el nombre y apellido
        label.config(text="Hilos con argumentos en Python " + nombre + " " + apellido)
        time.sleep(9)  # Espera 9 segundos
        label.config(text="Hilos con Python desde el hilo secundario")

    # Crear la ventana principal de Tkinter
    ventana = tk.Tk()
    ventana.title("Programa de Hilos con Tkinter")
    ventana.geometry("400x200")
    ventana.configure(bg="#34495e")  # Fondo gris oscuro

    # Crear una etiqueta para mostrar el progreso
    label = tk.Label(ventana, text="Esperando para ejecutar...", bg="#34495e", fg="#ffffff")
    label.pack(pady=10)

    # Crear campos de entrada para nombre y apellido
    nombre_label = tk.Label(ventana, text="Nombre:", bg="#34495e", fg="#ffffff")
    nombre_label.pack()
    nombre_entry = tk.Entry(ventana)
    nombre_entry.pack()

    apellido_label = tk.Label(ventana, text="Apellido:", bg="#34495e", fg="#ffffff")
    apellido_label.pack()
    apellido_entry = tk.Entry(ventana)
    apellido_entry.pack()

    # Crear un botón que inicia el hilo cuando se hace clic
    boton = tk.Button(ventana, text="Iniciar Hilo", command=lambda: threading.Thread(target=Hilo_02, args=(nombre_entry.get(), apellido_entry.get(), label), daemon=True).start(), bg="#3498db", fg="white")
    boton.pack(pady=20)

    # Iniciar el loop de la interfaz gráfica
    ventana.mainloop()

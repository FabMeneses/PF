import tkinter as tk
from queue import Queue
import random
import time

def ejecutar():
    # Tamaño máximo del buffer compartido
    BUFFER_SIZE = 5
    buffer = Queue(BUFFER_SIZE)

    # Variable de control para iniciar/detener procesos
    global running
    running = False

    # Función del Productor 
    def productor():
        if running:
            if not buffer.full():
                item = random.randint(1, 100)  # Generar un ítem aleatorio
                buffer.put(item)  # Colocar el ítem en la cola
                log_text.insert(tk.END, "⚽ ")
                log_text.insert(tk.END, "Productor", "bold")
                log_text.insert(tk.END, f" produjo: {item}\n")
                log_text.see(tk.END)  # Desplazar automáticamente el scroll
            root.after(1000, productor)  # Programar la próxima ejecución

    # Función del Consumidor
    def consumidor():
        if running:
            if not buffer.empty():
                item = buffer.get()  # Extraer el ítem de la cola
                log_text.insert(tk.END, "🐯 ")
                log_text.insert(tk.END, "Consumidor", "bold")
                log_text.insert(tk.END, f" consumió: {item}\n")
                log_text.see(tk.END)  # Desplazar automáticamente el scroll
                buffer.task_done()  # Marca el ítem como procesado
            root.after(1500, consumidor)  # Programar la próxima ejecución

    # Iniciar los procesos
    def iniciar():
        global running
        if not running:
            running = True
            status_label.config(text="Estado: Activo 🟡🔵", fg="blue")
            log_text.insert(tk.END, "🔥 Procesos iniciados...\n")
            productor()
            consumidor()

    # Detener los procesos
    def detener():
        global running
        if running:
            running = False
            status_label.config(text="Estado: Inactivo 🛑", fg="red")
            log_text.insert(tk.END, "🚫 Procesos detenidos...\n")

    # Configurar la ventana de Tkinter
    root = tk.Tk()
    root.title("Tigres Productor-Consumidor")
    root.geometry("550x500")
    root.config(bg="#FFDD00")  # Fondo amarillo Tigres

    # Crear el marco principal
    main_frame = tk.Frame(root, bg="#FFDD00")
    main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Log para mostrar la actividad
    log_frame = tk.LabelFrame(main_frame, text="Log de Actividad", font=("Arial", 12, "bold"), bg="#FFDD00", fg="#0033A0", bd=3, relief="ridge")
    log_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    log_text = tk.Text(log_frame, width=60, height=15, state=tk.NORMAL, bg="white", fg="black", font=("Consolas", 10), bd=2, relief="sunken")
    log_text.tag_config("bold", font=("Consolas", 10, "bold"))  # Configuración para negrita
    log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Barra de estado
    status_label = tk.Label(root, text="Estado: Inactivo 🛑", fg="red", bg="#FFDD00", font=("Arial", 12, "bold"), bd=1, relief="sunken", anchor="w")
    status_label.pack(pady=5, fill=tk.X, padx=10)

    # Botones para controlar los procesos
    button_frame = tk.Frame(root, bg="#FFDD00")
    button_frame.pack(pady=10)

    start_button = tk.Button(button_frame, text="Iniciar ⚽", command=iniciar, bg="#0033A0", fg="white", font=("Arial", 12, "bold"), width=12, relief="raised")
    start_button.grid(row=0, column=0, padx=10)

    stop_button = tk.Button(button_frame, text="Detener 🛑", command=detener, bg="#D50000", fg="white", font=("Arial", 12, "bold"), width=12, relief="raised")
    stop_button.grid(row=0, column=1, padx=10)

    # Ejecutar la aplicación
    root.mainloop()
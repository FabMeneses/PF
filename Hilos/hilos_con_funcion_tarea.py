import tkinter as tk
import threading
import time

def Tarea_Tiempo(Tarea, text_widget, duracion):
    inicio = time.time()
    text_widget.insert(tk.END, f"Inicio de la tarea {Tarea}\n", "inicio")
    time.sleep(duracion)
    tiempo_total = time.time() - inicio
    text_widget.insert(tk.END, f"Fin de la tarea {Tarea} Duracion: {tiempo_total:.2f}\n", "fin")

def iniciar_tareas(text_widget):
    def run_tasks():
        hilo1 = threading.Thread(target=Tarea_Tiempo, args=("Tarea 1", text_widget, 2))
        hilo2 = threading.Thread(target=Tarea_Tiempo, args=("Tarea 2", text_widget, 4))

        hilo1.start()
        hilo2.start()

        hilo1.join()
        hilo2.join()

        text_widget.insert(tk.END, "Fin del programa\n", "fin_programa")

    threading.Thread(target=run_tasks).start()

def ejecutar():
    principal()

def principal():
    root = tk.Tk()
    root.title("Ejemplo de Hilos con Tkinter")
    root.configure(bg="#34495e")  # Fondo oscuro para la ventana principal

    text_widget = tk.Text(root, height=10, width=50, bg="#34495e", fg="#ffffff", insertbackground="#ffffff")
    text_widget.pack(pady=20)

    # Configuración de colores para el text_widget
    text_widget.tag_config("inicio", foreground="white")
    text_widget.tag_config("fin", foreground="white")
    text_widget.tag_config("fin_programa", foreground="white")

    btn_iniciar = tk.Button(root, text="Iniciar Tareas", command=lambda: iniciar_tareas(text_widget), bg="#3498db", fg="#ffffff")
    btn_iniciar.pack(pady=20)

    # Asegurarse de que todas las letras sean blancas
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(fg="#ffffff")

    root.mainloop()

# Función para crear una ventana emergente
def crear_ventana_emergente():
    ventana = tk.Toplevel()
    ventana.configure(bg="#2c3e50")  # Fondo gris claro para la ventana emergente

    etiqueta = tk.Label(ventana, text="Ventana Emergente", bg="#2c3e50", fg="#ffffff")
    etiqueta.pack(pady=10)

    btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg="#e74c3c", fg="#ffffff", relief="flat", borderwidth=0)
    btn_cerrar.pack(pady=10)

if __name__ == "__main__":
    ejecutar()

import tkinter as tk
import threading
import time
import random

def enviar_documento(equipo_id, texto_area):
    paginas = random.randint(1, 10)
    if texto_area.winfo_exists():
        texto_area.insert(tk.END, f"Equipo {equipo_id} tiene un documento de {paginas} páginas.\n", "info")
        texto_area.yview(tk.END)
    
    with semaforo_impresora:
        if texto_area.winfo_exists():
            texto_area.insert(tk.END, f"Equipo {equipo_id} está enviando el documento a la impresora.\n", "sending")
            texto_area.yview(tk.END)
        time.sleep(paginas)
        if texto_area.winfo_exists():
            texto_area.insert(tk.END, f"Equipo {equipo_id} ha terminado de imprimir.\n", "done")
            texto_area.yview(tk.END)

def iniciar_impresion(texto_area):
    equipos = 6
    threads = []
    
    for equipo_id in range(1, equipos + 1):
        t = threading.Thread(target=enviar_documento, args=(equipo_id, texto_area))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

def Iniciar():
    ventana = tk.Tk()
    ventana.title("Simulación de Impresora")
    ventana.configure(bg="#34495e")  # Fondo gris oscuro

    texto_area = tk.Text(ventana, height=15, width=60, bg="#34495e", fg="#ffffff", insertbackground="#ffffff")  # Fondo gris oscuro y texto blanco
    texto_area.pack(padx=10, pady=10)

    # Definir estilos de texto
    texto_area.tag_config("info", foreground="white")
    texto_area.tag_config("sending", foreground="White")
    texto_area.tag_config("done", foreground="White")

    boton_comenzar = tk.Button(ventana, text="Comenzar Simulación", command=lambda: threading.Thread(target=iniciar_impresion, args=(texto_area,), daemon=True).start(), bg="#3498db", fg="#ffffff", activebackground="#2980b9", activeforeground="#ffffff", relief="flat")
    boton_comenzar.pack(pady=10)

    ventana.mainloop()

def ejecutar():
    global semaforo_impresora
    semaforo_impresora = threading.Semaphore(2)
    Iniciar()

if __name__ == "__main__":
    ejecutar()

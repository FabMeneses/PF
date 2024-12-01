import tkinter as tk
from tkinter import font, Toplevel
from PIL import Image, ImageTk
import fitz
import os

from Hilos import hilos_hilos, hilos_con_argumentos, hilos_con_funcion_tarea, hilos_sincronizados, mario_bros_ruleta
from Sockets import mensajes_cliente_servidor, tcp_cliente_servidor, udp_cliente_servidor, comunicacion_directa, comunicacion_indirecta, autenticacion_aguila
from Semaforos import condicion_de_carrera, sala_de_chat_ip_cliente, sala_de_chat_ip_servidor, sincronizacion_de_semaforos, semaforos_cliente_servidor, barbero_dormilon, barbero_dormilon_cliente_servidor, sala_de_chat_local
from Patrones import productor_consumidor, actores, reactor_y_proactor, futuro_promesa_cliente, futuro_promesa_servidor

ventanas_abiertas = []

PDF_PATHS = {
    "Documentación Del Proyecto Final": r"Documentacion/pdfproyectofinal.pdf",
    "Apunte De Introduccion A La Programacion Concurrente": r"Documentacion\Apunte_de_Introducción_de_Concurrencia.pdf",
    "Apunte De Hilos": r"Documentacion\Apunte_de_Hilos.pdf",
    "Apunte de Expectativas De La Materia": r"Documentacion\Apunte_expectativas_de_la_materia.pdf",
    "Apunte De Sockets TCP y UDP": r"Documentacion\ApunteSockets_TCP_y_UDP.pdf",
    "Apunte De Semáforos": r"Documentacion\Apunte_Semáforos.pdf",
    "Apunte De Tkinter": r"Documentacion\Apunte_Tkinter.pdf",
    "Apunte De Sala De Chat Simple": r"Documentacion\Apunte_Sala_De_Chat_Simple.pdf",
    "Apunte De Patron Future Y Promesa": r"Documentacion\Apunte_Introducción_a_los_patrones_y_el_Patrón_de_Futuro_y_Promesa.pdf",
    "Apunte De Patron Productor/Consumidor": r"Documentacion\Apunte_Patrón_de_Productor_Consumidor.pdf",
    "Apunte De Patron De Actores": r"Documentacion\Apunte_Patrón_de_El_Modelo_de_Actores .pdf",
    "Apunte de Patron Reactor Y Proactor": r"Documentacion\Apunte_Patrón_de_Reactor_y_Proactor.pdf"
}

def mostrar_pdf(pdf_path):
    ventana_pdf = Toplevel(root)
    ventanas_abiertas.append(ventana_pdf)
    ventana_pdf.title(os.path.basename(pdf_path)) 
    ventana_pdf.geometry("650x600")
    ventana_pdf.configure(bg="#2c3e50")

    frame = tk.Frame(ventana_pdf, bg="#2c3e50")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="white")
    scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)

    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def load_pdf():
        try:
            doc = fitz.open(pdf_path)
            for page_number in range(len(doc)):
                page = doc.load_page(page_number)
                pix = page.get_pixmap()
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                photo = ImageTk.PhotoImage(image)

                label = tk.Label(inner_frame, image=photo, bg="white")
                label.image = photo
                label.pack()

            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        except Exception as e:
            tk.Label(inner_frame, text=f"Error al cargar el PDF:\n{e}", fg="red", bg="white").pack()

    load_pdf()

opciones_funciones = {
    "Hilos-Hilos": hilos_hilos.ejecutar if hasattr(hilos_hilos, 'ejecutar') else lambda: print("Función no encontrada"),
    "Hilos con argumentos": hilos_con_argumentos.ejecutar if hasattr(hilos_con_argumentos, 'ejecutar') else lambda: print("Función no encontrada"),
    "Hilos con función tarea": hilos_con_funcion_tarea.ejecutar if hasattr(hilos_con_funcion_tarea, 'ejecutar') else lambda: print("Función no encontrada"),
    "Hilos sincronizados": hilos_sincronizados.ejecutar if hasattr(hilos_sincronizados, 'ejecutar') else lambda: print("Función no encontrada"),
    "Mario Bros Ruleta": mario_bros_ruleta.main if hasattr(mario_bros_ruleta, 'main') else lambda: print("Función no encontrada"),
    "Mensajes Cliente/Servidor": mensajes_cliente_servidor.ejecutar if hasattr(mensajes_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "TCP Cliente/Servidor": tcp_cliente_servidor.ejecutar if hasattr(tcp_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "UDP Cliente/Servidor": udp_cliente_servidor.ejecutar if hasattr(udp_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Sincronización de semáforos": sincronizacion_de_semaforos.ejecutar if hasattr(sincronizacion_de_semaforos, 'ejecutar') else lambda: print("Función no encontrada"),
    "Barbero dormilón": barbero_dormilon.ejecutar if hasattr(barbero_dormilon, 'ejecutar') else lambda: print("Función no encontrada"),
    "Sala de chat IP Cliente": sala_de_chat_ip_cliente.ejecutar if hasattr(sala_de_chat_ip_cliente, 'ejecutar') else lambda: print("Función no encontrada"),
    "Sala de chat IP Servidor": sala_de_chat_ip_servidor.ejecutar if hasattr(sala_de_chat_ip_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Productor-Consumidor": productor_consumidor.ejecutar if hasattr(productor_consumidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Reactor y Proactor": reactor_y_proactor.ejecutar if hasattr(reactor_y_proactor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Comunicacion Directa": comunicacion_directa.ejecutar if hasattr(comunicacion_directa, 'ejecutar') else lambda: print("Función no encontrada"),
    "Comunicacion Indirecta": comunicacion_indirecta.ejecutar if hasattr(comunicacion_indirecta, 'ejecutar') else lambda: print("Función no encontrada"),
    "Autenticacion Aguila": autenticacion_aguila.ejecutar if hasattr(autenticacion_aguila, 'ejecutar') else lambda: print("Función no encontrada"),
    "Semaforos Cliente/Servidor": semaforos_cliente_servidor.ejecutar if hasattr(semaforos_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Sala de Chat Local": sala_de_chat_local.ejecutar if hasattr(sala_de_chat_local, 'ejecutar') else lambda: print("Función no encontrada"),
    "Condicion de Carrera": condicion_de_carrera.ejecutar if hasattr(condicion_de_carrera, 'ejecutar') else lambda: print("Función no encontrada"),
    "Actores": actores.ejecutar if hasattr(actores, 'ejecutar') else lambda: print("Función no encontrada"),
    "Futuro Promesa Cliente": futuro_promesa_cliente.ejecutar if hasattr(futuro_promesa_cliente, 'ejecutar') else lambda: print("Función no encontrada"),
    "Futuro Promesa Servidor": futuro_promesa_servidor.ejecutar if hasattr(futuro_promesa_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Barbero dormilón Cliente/Servidor": barbero_dormilon_cliente_servidor.ejecutar if hasattr(barbero_dormilon_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
}

def mostrar_submenu(titulo, opciones):
    for widget in root.winfo_children():
        if widget != menu_bar:
            widget.destroy()

    frame = tk.Frame(root, bg="#2c3e50")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    for opcion in opciones:
        if titulo == "Documentación":
            tk.Button(frame, text=opcion, command=lambda opt=opcion: mostrar_pdf(PDF_PATHS[opt]), 
                      bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=5, pady=5).pack(pady=5)
        else:
            tk.Button(frame, text=opcion, command=opciones_funciones.get(opcion, lambda: print("Función no encontrada")),
                      bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=5, pady=5).pack(pady=5)

    frame.update_idletasks()
    frame_width = frame.winfo_width()
    for button in frame.winfo_children():
        button_width = button.winfo_reqwidth()
        button.pack_configure(padx=(frame_width - button_width) // 2)

def cerrar_aplicacion():
    for ventana in ventanas_abiertas:
        if ventana.winfo_exists():
            ventana.destroy()
    root.destroy()
    os._exit(0)

def mostrar_acerca_de():
    ventana_acerca_de = Toplevel(root)
    ventana_acerca_de.title("Acerca de")
    ventana_acerca_de.geometry("600x250")
    ventana_acerca_de.configure(bg="#2c3e50")

    frame = tk.Frame(ventana_acerca_de, bg="#2c3e50", padx=20, pady=20)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    label_titulo = tk.Label(frame, text="Programación Concurrente UPP SFTW_07_03", bg="#2c3e50", fg="white", font=("Helvetica", 14, "bold"))
    label_titulo.pack(pady=(0, 10))

    integrantes = [
        "1.- Fabricio Meneses Avila. Matricula: 2231122171",
        "2.- Jorge Ruiz Diaz. Matricula: 2231122197",
        "3.- Diego Daniel Magdaleno Medina. Matricula: 2231122172",
        "4.- Angel Gabriel Castillo Sanchez. Matricula: 2231122204",
        "5.- Josefa Francisco Hernandez. Matricula: 2231122164"
    ]

    for integrante in integrantes:
        tk.Label(frame, text=integrante, bg="#2c3e50", fg="white", font=("Helvetica", 10)).pack(anchor="w")

    tk.Button(frame, text="Cerrar", command=ventana_acerca_de.destroy, bg="#e74c3c", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=10, pady=5).pack(pady=(20, 0))

root = tk.Tk()
root.title("Programación Concurrente UPP SFTW_07_03")
root.geometry("800x600")
root.configure(bg="#34495e")
root.state('zoomed')

bg_image = Image.open("Imagenes/BG.png")
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

menu_bar = tk.Frame(root, bg="#2c3e50")
menu_bar.pack(side="top", fill="x")
menu_bar.lift()

hilos_opciones = ["Hilos-Hilos", "Hilos con argumentos", "Hilos con función tarea", "Hilos sincronizados", "Mario Bros Ruleta"]
sockets_opciones = ["Mensajes Cliente/Servidor", "TCP Cliente/Servidor", "UDP Cliente/Servidor", "Comunicacion Directa", "Comunicacion Indirecta", "Autenticacion Aguila"]
semaforos_opciones = ["Sincronización de semáforos", "Barbero dormilón", "Barbero dormilón Cliente/Servidor", "Condicion de Carrera", "Semaforos Cliente/Servidor", "Sala de Chat Local", "Sala de chat IP Cliente", "Sala de chat IP Servidor"]
patrones_opciones = ["Productor-Consumidor", "Actores", "Reactor y Proactor", "Futuro Promesa Cliente", "Futuro Promesa Servidor"]
documentacion_opciones = ["Apunte De Introduccion A La Programacion Concurrente", "Apunte De Hilos", "Apunte De Sockets TCP y UDP", "Apunte De Semáforos", "Apunte De Tkinter", "Apunte De Sala De Chat Simple", "Apunte De Patron Future Y Promesa", "Apunte De Patron Productor/Consumidor", "Apunte De Patron De Actores", "Apunte de Patron Reactor Y Proactor", "Apunte de Expectativas De La Materia", "Documentación Del Proyecto Final"]

menu_font = font.Font(family="Helvetica", size=12, weight="bold")
boton_estilo = {"bg": "#3498db", "fg": "white", "font": menu_font, "bd": 0, "padx": 10, "pady": 10}

tk.Button(menu_bar, text="Hilos", command=lambda: mostrar_submenu("Hilos", hilos_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Sockets", command=lambda: mostrar_submenu("Sockets", sockets_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Semáforos", command=lambda: mostrar_submenu("Semáforos", semaforos_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Patrones", command=lambda: mostrar_submenu("Patrones", patrones_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Documentación", command=lambda: mostrar_submenu("Documentación", documentacion_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Acerca de", command=mostrar_acerca_de, **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Salir", command=cerrar_aplicacion, **boton_estilo).pack(side="left", expand=True, fill="x")

menu_bar.lift()

root.mainloop()

#DEDICATORIA AL KEBIN
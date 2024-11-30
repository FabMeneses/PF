import tkinter as tk
import random
import threading
import time

symbols = ["🌼", "🍄", "🌟"]

class MarioRuletaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mario Bros Ruleta")
        self.root.geometry("400x250")
        self.root.configure(bg="#34495e")  # Fondo oscuro

        # Variables para el estado del juego
        self.result = [''] * 3
        self.hilado_flags = [True] * 3
        self.threads = []
        self.score = 0

        # Crear y organizar los widgets de la interfaz
        self.create_widgets()

        # Evento para alternar entre iniciar y detener los giros con la tecla Enter
        self.root.bind("<Return>", self.toggle_spin_event)

    def create_widgets(self):
        """Crea y organiza los widgets de la interfaz."""
        self.label_title = tk.Label(self.root, text="Ruleta Mario Bros", font=("Arial", 20, "bold"), fg="#ffffff", bg="#34495e")
        self.label_title.pack(pady=10)

        self.label_result = tk.Label(self.root, text="Tiradas: --- --- ---", font=("Arial", 16), fg="#ffffff", bg="#34495e")
        self.label_result.pack(pady=10)

        self.label_score = tk.Label(self.root, text="Puntos: 0", font=("Arial", 16), fg="#ffffff", bg="#34495e")
        self.label_score.pack(pady=10)

        self.button_toggle = tk.Button(self.root, text="Tirar", command=self.toggle_spin, font=("Arial", 14), bg="#3498db", fg="white", width=15, relief="flat")
        self.button_toggle.pack(pady=10)

    def pantalla_giro(self, index):
        """Simula el giro de un tambor."""
        while self.hilado_flags[index]:
            self.result[index] = random.choice(symbols)
            self.update_result_label()
            time.sleep(0.5)  # Velocidad del giro

    def start_spin(self):
        """Inicia los giros de los tambores."""
        self.button_toggle.config(text="Detener", bg="#e74c3c")
        self.result = [''] * 3
        self.hilado_flags = [True] * 3
        self.threads = []

        for i in range(3):
            thread = threading.Thread(target=self.pantalla_giro, args=(i,))
            self.threads.append(thread)
            thread.start()

        self.label_result.config(text="Gira presionando Enter para detener cada tambor.")

    def stop_spin(self):
        """Detiene un tambor."""
        for i in range(3):
            if self.hilado_flags[i]:
                self.hilado_flags[i] = False
                self.threads[i].join()
                if i == 2:  # Último tambor detenido
                    self.check_result()
                    self.button_toggle.config(text="Volver a iniciar", bg="#2196F3")
                return

    def toggle_spin_event(self, event):
        """Alterna entre iniciar y detener los giros al presionar Enter."""
        self.toggle_spin()

    def toggle_spin(self):
        """Alterna entre iniciar y detener los giros al presionar el botón."""
        if self.button_toggle.cget("text") == "Tirar":
            self.start_spin()
        elif self.button_toggle.cget("text") == "Detener":
            self.stop_spin()
        else:
            self.reset_game()

    def update_result_label(self):
        """Actualiza la etiqueta con los resultados actuales."""
        self.label_result.config(text=f"Giros: {' '.join(self.result)}")

    def check_result(self):
        """Calcula el puntaje y muestra el resultado."""
        score_gain = self.calcula_score(self.result)
        self.score += score_gain
        if score_gain > 0:
            self.label_score.config(text=f"¡Ganaste tienes {score_gain} puntos! Total: {self.score} Puntos")
        else:
            self.label_score.config(text=f"Una lastima. Tienes: {self.score} Puntos")

    def calcula_score(self, result):

        if result[0] == result[1] == result[2]:
            if result[0] == "🌟":
                return 5
            elif result[0] == "🌼":
                return 3
            elif result[0] == "🍄":
                return 2
        return 0

    def reset_game(self):
        self.result = [''] * 3
        self.hilado_flags = [True] * 3
        self.label_result.config(text="Giros: --- --- ---")
        self.button_toggle.config(text="Tirar", bg="#4CAF50")

def main():
    root = tk.Tk()
    app = MarioRuletaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
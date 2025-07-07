import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.graph_utils import update_graphs


class AppView:
    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Configura los elementos de la interfaz de usuario"""
        self.root.title("Algoritmos de Ordenamiento y Búsqueda")
        self.root.geometry("1000x700")

        # Configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variables de control
        self.search_value = ctk.StringVar()
        self.algorithm_choice = ctk.StringVar(value="quicksort")
        self.execution_time = ctk.StringVar(value="Tiempo: -")
        self.search_result = ctk.StringVar(value="Resultado: -")

        # Configurar layout
        self.setup_main_layout()

    def setup_main_layout(self):
        """Configura el layout principal"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel de control izquierdo
        self.setup_control_panel()

        # Panel de visualización derecha
        self.setup_visualization_panel()

    def setup_control_panel(self):
        """Configura el panel de control izquierdo"""
        self.control_panel = ctk.CTkFrame(self.main_frame, width=300)
        self.control_panel.pack(side="left", fill="y", padx=5, pady=5)

        # Título
        title_label = ctk.CTkLabel(self.control_panel, text="Algoritmos", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Selección de algoritmo
        self.setup_algorithm_selection()

        # Generación de datos
        self.setup_data_generation()

        # Búsqueda
        self.setup_search_section()

        # Botones de acción
        self.setup_action_buttons()

        # Información de resultados
        self.setup_result_info()

        #animaciones?
        #self.setup_animation_controls()

    def setup_algorithm_selection(self):
        """Configura la selección de algoritmo"""
        algo_frame = ctk.CTkFrame(self.control_panel)
        algo_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(algo_frame, text="Seleccionar algoritmo:").pack(anchor="w")
        ctk.CTkRadioButton(algo_frame, text="Random QuickSort", variable=self.algorithm_choice,
                           value="quicksort").pack(anchor="w", padx=5)
        ctk.CTkRadioButton(algo_frame, text="Búsqueda Secuencial Ordenada", variable=self.algorithm_choice,
                           value="sequential").pack(anchor="w", padx=5)

    def setup_data_generation(self):
        """Configura la generación de datos"""
        data_frame = ctk.CTkFrame(self.control_panel)
        data_frame.pack(fill="x", padx=5, pady=10)

        ctk.CTkLabel(data_frame, text="Generar datos:").pack(anchor="w")

        self.data_size_entry = ctk.CTkEntry(data_frame, placeholder_text="Tamaño de lista")
        self.data_size_entry.pack(fill="x", padx=5, pady=5)

        generate_btn = ctk.CTkButton(data_frame, text="Generar Aleatoria", command=self.on_generate_data)
        generate_btn.pack(fill="x", padx=5, pady=5)

        self.manual_data_entry = ctk.CTkEntry(data_frame, placeholder_text="Ingresar datos (ej: 5,3,7,1)")
        self.manual_data_entry.pack(fill="x", padx=5, pady=5)

        manual_btn = ctk.CTkButton(data_frame, text="Usar Datos Ingresados", command=self.on_manual_data)
        manual_btn.pack(fill="x", padx=5, pady=5)

    def setup_search_section(self):
        """Configura la sección de búsqueda"""
        self.search_frame = ctk.CTkFrame(self.control_panel)
        self.search_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(self.search_frame, text="Valor a buscar:").pack(anchor="w")
        search_entry = ctk.CTkEntry(self.search_frame, textvariable=self.search_value)
        search_entry.pack(fill="x", padx=5, pady=5)

        # Actualizar visibilidad según algoritmo seleccionado
        self.algorithm_choice.trace_add("write", self.update_search_visibility)
        self.update_search_visibility()

    def setup_action_buttons(self):
        """Configura los botones de acción"""
        execute_btn = ctk.CTkButton(self.control_panel, text="Ejecutar Algoritmo",
                                    command=self.on_execute_algorithm)
        execute_btn.pack(fill="x", padx=5, pady=10)

        clear_btn = ctk.CTkButton(self.control_panel, text="Limpiar Resultados",
                                  command=self.on_clear_results)
        clear_btn.pack(fill="x", padx=5, pady=10)

    def setup_result_info(self):
        """Configura la visualización de resultados"""
        time_label = ctk.CTkLabel(self.control_panel, textvariable=self.execution_time)
        time_label.pack(pady=5)

        result_label = ctk.CTkLabel(self.control_panel, textvariable=self.search_result)
        result_label.pack(pady=5)

    def setup_visualization_panel(self):
        """Configura el panel de visualización de datos"""
        self.visualization_panel = ctk.CTkFrame(self.main_frame)
        self.visualization_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Frame para gráficos
        self.graph_frame = ctk.CTkFrame(self.visualization_panel)
        self.graph_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Títulos para los gráficos
        titles_frame = ctk.CTkFrame(self.visualization_panel)
        titles_frame.pack(fill="x", padx=5, pady=5)

        self.original_title = ctk.CTkLabel(titles_frame, text="Datos Originales", font=("Arial", 12))
        self.original_title.pack(side="left", expand=True)

        self.result_title = ctk.CTkLabel(titles_frame, text="Resultado", font=("Arial", 12))
        self.result_title.pack(side="right", expand=True)

        # Inicializar gráficos
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Mostrar gráficos vacíos inicialmente
        self.update_graphs([], [])

    def update_search_visibility(self, *args):
        """Actualiza la visibilidad de la sección de búsqueda"""
        if self.algorithm_choice.get() == "sequential":
            self.search_frame.pack(fill="x", padx=5, pady=5)
            self.result_title.configure(text="Lista Ordenada")
        else:
            self.search_frame.pack_forget()
            # self.result_title.configure(text="Lista Ordenada")
            self.search_result.set("Resultado: -")

    # Métodos de callback
    def on_generate_data(self):
        if self.controller and hasattr(self.controller, 'handle_generate_data'):
            try:
                size = int(self.data_size_entry.get())
                self.controller.handle_generate_data(size)
            except ValueError:
                self.show_error("Ingrese un número válido para el tamaño")

    def on_manual_data(self):
        if self.controller and hasattr(self.controller, 'handle_manual_data'):
            self.controller.handle_manual_data(self.manual_data_entry.get())

    def on_execute_algorithm(self):
        if self.controller and hasattr(self.controller, 'handle_execute_algorithm'):
            algorithm = self.algorithm_choice.get()
            search_value = self.search_value.get() if algorithm == "sequential" else None
            self.controller.handle_execute_algorithm(algorithm, search_value)

    def on_clear_results(self):
        if self.controller and hasattr(self.controller, 'handle_clear_results'):
            self.controller.handle_clear_results()

    # Métodos para establecer callbacks
    def set_generate_data_callback(self, callback):
        self.controller.handle_generate_data = callback

    def set_manual_data_callback(self, callback):
        self.controller.handle_manual_data = callback

    def set_execute_algorithm_callback(self, callback):
        self.controller.handle_execute_algorithm = callback

    def set_clear_results_callback(self, callback):
        self.controller.handle_clear_results = callback

    # Métodos de visualización
    def update_graphs(self, original_data, result_data, highlight_index=None):
        """Actualiza los gráficos con los datos proporcionados"""
        self.ax1.clear()
        self.ax2.clear()

        # Gráfico de datos originales
        if original_data:
            self.ax1.bar(range(len(original_data)), original_data, color='blue')
            self.ax1.set_title("Datos Originales")
            self.ax1.set_xlabel("Índice")
            self.ax1.set_ylabel("Valor")

        # Gráfico de resultados
        if result_data:
            colors = ['green'] * len(result_data)
            if highlight_index is not None and highlight_index != -1:
                colors[highlight_index] = 'red'
            self.ax2.bar(range(len(result_data)), result_data, color=colors)
            self.ax2.set_title("Lista Ordenada")
            self.ax2.set_xlabel("Índice")
            self.ax2.set_ylabel("Valor")

        self.canvas.draw()

    def setup_animation_controls(self):
        """Controles para la animación paso a paso"""
        self.animation_frame = ctk.CTkFrame(self.control_panel)
        self.animation_frame.pack(fill="x", padx=5, pady=10)

        self.step_button = ctk.CTkButton(self.animation_frame, text="Paso Siguiente",
                                         state="disabled", command=self.next_step)
        self.step_button.pack(side="left", expand=True)

        self.play_button = ctk.CTkButton(self.animation_frame, text="Reproducir",
                                         state="disabled", command=self.play_animation)
        self.play_button.pack(side="right", expand=True)

        self.speed_slider = ctk.CTkSlider(self.control_panel, from_=100, to=1000,
                                          command=self.set_animation_speed)
        self.speed_slider.set(500)
        self.speed_slider.pack(fill="x", padx=5, pady=5)

        self.current_step = 0
        self.animation_steps = []
        self.animation_speed = 500
        self.animation_running = False

    def show_results(self, sorted_data, time_text, result_text="Resultado: -", highlight_index=None):
        """Muestra los resultados del algoritmo"""
        self.execution_time.set(time_text)
        self.search_result.set(result_text)
        self.update_graphs(self.controller.data_handler.data, sorted_data, highlight_index)

    def clear_results(self):
        """Limpia los resultados visuales"""
        self.execution_time.set("Tiempo: -")
        self.search_result.set("Resultado: -")

    def show_message(self, message):
        """Muestra un mensaje informativo"""
        messagebox.showinfo("Información", message)

    def show_error(self, error_message):
        """Muestra un mensaje de error"""
        messagebox.showerror("Error", error_message)
from models.algoritmos import random_quicksort, ordered_sequential_search
from models.data_handler import DataHandler
from views.app_view import AppView
import time


class SortingSearchingApp:
    def __init__(self, root):
        self.root = root
        self.data_handler = DataHandler()
        self.view = AppView(root, self)

        # Configurar manejadores de eventos
        self.setup_event_handlers()

    def setup_event_handlers(self):
        """Configura los manejadores de eventos para la vista"""
        self.view.set_generate_data_callback(self.handle_generate_data)
        self.view.set_manual_data_callback(self.handle_manual_data)
        self.view.set_execute_algorithm_callback(self.handle_execute_algorithm)
        self.view.set_clear_results_callback(self.handle_clear_results)

    def handle_generate_data(self, size):
        """Maneja la generación de datos aleatorios"""
        try:
            self.data_handler.generate_random_data(size)
            self.view.update_graphs(self.data_handler.data, [])
            self.view.show_message("Datos generados exitosamente")
        except ValueError as e:
            self.view.show_error(str(e))

    def handle_manual_data(self, data_str):
        """Maneja el ingreso manual de datos"""
        try:
            self.data_handler.set_manual_data(data_str)
            self.view.update_graphs(self.data_handler.data, [])
            self.view.show_message("Datos establecidos correctamente")
        except ValueError as e:
            self.view.show_error(str(e))

    def handle_execute_algorithm(self, algorithm, search_value=None):
        """Maneja la ejecución del algoritmo seleccionado"""
        if not self.data_handler.data:
            self.view.show_error("Primero genere o ingrese datos")
            return

        try:
            start_time = time.time()

            if algorithm == "quicksort":
                sorted_data = random_quicksort(self.data_handler.data.copy())
                self.data_handler.sorted_data = sorted_data
                execution_time = (time.time() - start_time) * 1000
                self.view.show_results(sorted_data, f"Tiempo: {execution_time:.2f} ms")

            elif algorithm == "sequential":
                if not self.data_handler.sorted_data:
                    self.data_handler.sorted_data = random_quicksort(self.data_handler.data.copy())

                if search_value is None:
                    self.view.show_error("Ingrese un valor a buscar")
                    return

                try:
                    value = int(search_value)
                    result_index = ordered_sequential_search(self.data_handler.sorted_data, value)
                    execution_time = (time.time() - start_time) * 1000

                    if result_index != -1:
                        result_text = f"Encontrado en posición {result_index}"
                    else:
                        result_text = "No encontrado"

                    self.view.show_results(
                        self.data_handler.sorted_data,
                        f"Tiempo: {execution_time:.2f} ms",
                        result_text,
                        highlight_index=result_index
                    )
                except ValueError:
                    self.view.show_error("El valor a buscar debe ser un número")

        except Exception as e:
            self.view.show_error(f"Error durante la ejecución: {str(e)}")

    def handle_clear_results(self):
        """Maneja la limpieza de resultados"""
        self.data_handler.clear_results()
        self.view.update_graphs(self.data_handler.data, [])
        self.view.clear_results()
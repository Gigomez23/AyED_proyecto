import random


class DataHandler:
    def __init__(self):
        self.data = []
        self.sorted_data = []

    def generate_random_data(self, size):
        """Genera una lista aleatoria de datos"""
        if size <= 0:
            raise ValueError("El tamaño debe ser un número positivo")

        self.data = [random.randint(1, 100) for _ in range(size)]
        self.sorted_data = []

    def set_manual_data(self, data_str):
        """Establece los datos ingresados manualmente"""
        numbers = [int(x.strip()) for x in data_str.split(",") if x.strip()]

        if not numbers:
            raise ValueError("Ingrese al menos un número")

        self.data = numbers
        self.sorted_data = []

    def clear_results(self):
        """Limpia los resultados pero mantiene los datos originales"""
        self.sorted_data = []
import matplotlib.pyplot as plt


def update_graphs(ax1, ax2, original_data, result_data, highlight_index=None):
    """Actualiza los gráficos con los datos proporcionados"""
    ax1.clear()
    ax2.clear()

    # Gráfico de datos originales
    if original_data:
        ax1.bar(range(len(original_data)), original_data, color='blue')
        ax1.set_title("Datos Originales")
        ax1.set_xlabel("Índice")
        ax1.set_ylabel("Valor")

    # Gráfico de resultados
    if result_data:
        colors = ['green'] * len(result_data)
        if highlight_index is not None and highlight_index != -1:
            colors[highlight_index] = 'red'
        ax2.bar(range(len(result_data)), result_data, color=colors)
        ax2.set_title("Lista Ordenada")
        ax2.set_xlabel("Índice")
        ax2.set_ylabel("Valor")
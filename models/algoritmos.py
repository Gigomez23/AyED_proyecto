import random


def random_quicksort(arr):
    """Implementación de Random QuickSort"""
    if len(arr) <= 1:
        return arr

    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    return random_quicksort(less) + equal + random_quicksort(greater)



def ordered_sequential_search(arr, value):
    """Implementación de búsqueda secuencial ordenada"""
    for i, num in enumerate(arr):
        if num == value:
            return i
        elif num > value:
            break  # No es necesario seguir buscando
    return -1


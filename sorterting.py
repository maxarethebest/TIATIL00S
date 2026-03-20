# import random

# lista_1 = [1, 3, 5, 2, 4]

# def bogosort(osorterad_lista):
#     kontroll_lista = sorted(osorterad_lista)
    
#     osorterad = True
#     while osorterad:
#         sorterad_lista = []
#         for _ in range(len(osorterad_lista)):
#             idx = random.randint(0, len(osorterad_lista)-1)
#             sorterad_lista.append(osorterad_lista[idx])
#             osorterad_lista.pop(idx)
#         if sorterad_lista == kontroll_lista:
#             osorterad = False
#     return sorterad_lista

# print(bogosort(lista_1))


# lista_1 = [1, 3, 5, 2, 4]

# def customsort(osorterad_lista):
#     sorterad_lista = []
#     for _ in range(len(osorterad_lista)):
#         sorterad_lista.append(min(osorterad_lista))
#         osorterad_lista.remove(min(osorterad_lista))
#     return sorterad_lista

# print(customsort(lista_1))

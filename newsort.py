unsorted = [1, 4, 7, 2, 5, 8, 3, 0, 6, 9, -1, -3, -2]

def sortera(unsorted):
    empty_list = []

    for _ in range(len(unsorted)):
        maximum = min(unsorted) - 1
        for i in unsorted:
            if i > maximum:
                maximum = i
        empty_list.append(maximum)
        unsorted.remove(maximum)
    empty_list.reverse()
    return empty_list

print(sortera(unsorted))
matrix = []
list = []

for j in range(10):
    for i in range(10):
        i += 1 + (j * 10)
        var = str(i)
        if len(var) < 2:
            var = "00" + var
        elif len(var) < 3:
            var = "0" + var
        list.append(var)
    matrix.append(list)
    list = []

for i in matrix:
    print(i)
    
row = int(input("Vilken rad vill du ändra?: ")) - 1
column = int(input("Vilken kolumn vill du ändra?: ")) - 1
new_var = input("Vad vill du att det ska stå?: ")
matrix[row][column] = new_var

for i in matrix:
    print(i)
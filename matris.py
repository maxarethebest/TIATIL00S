matrix_1 = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]

matrix_2 = [[10, 11],
            [12, 13],
            [14, 15]]


def draw_matrix(matrix):
    print(matrix)
    print("┌", end= "")
    for i in matrix[0]:
        print("──", end= "")
    print("─", end="")
    print("┐")
    for i in matrix:
        print("│", end=" ")
        for j in i:
            print(j, end=" ")
        print("│")
    print("└", end= "")
    for i in matrix[0]:
        print("──", end= "")
    print("─", end="")
    print("┘")  
    
def create_matrix():
    matrix = []
    while True:
        try:
            rows = int(input("Mata in antal rader: "))
            columns = int(input("Mata in antal kolumner: "))
            
            for i in range(rows):
                row = []
                
                for j in range(columns):
                    tal = int(input(f"Mata in det {j+1}:a talet i den {i+1}:a raden: "))
                    row.append(tal)
                    
                matrix.append(row)
            break
        except:
            print("Error: Kontrollera inmatning")
        
    print("Du har nu skapat matrisen:\n")
    draw_matrix(matrix)
    return matrix                
    
def calculate_matrix_dimensions(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    return rows, columns

def check_possibility(matrix_1_dimensions, matrix_2_dimensions):
    if matrix_1_dimensions[1] == matrix_2_dimensions[0]:
        return True
    else:
        return False




# print(check_possibility(calculate_matrix_dimensions(create_matrix()), calculate_matrix_dimensions(matrix_2)))

def multiply_matrixes(matrix_1, matrix_2):
    new_matrix = []
    new_row = []
    sum = 0
    shared_length = calculate_matrix_dimensions(matrix_2)[0]
    for columns in range(shared_length):
        sum = 0
        for rows in range(shared_length):
            
            sum += matrix_1[columns][rows] * matrix_2[columns][rows]
        new_row.append(sum)
        new_matrix.append(new_row)
        print(new_matrix)
            # 0,0 * 0,0 + 0,1 * 1,0 + 0,2 * 2,0
            # 0,0 * 1,1 + 0,1 * 1,1 + 0,2 * 2,1
            # 1,0 * 0,0 + 1,1 * 1,0 + 1,2 * 2,0
multiply_matrixes(matrix_1, matrix_2)

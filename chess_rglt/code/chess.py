board = [[" " for _ in range(8)] for _ in range(8)]



# ranks = ["a", "b", "c", "d", "e", "f", "g", "h"]
# files = ["1", "2", "3", "4", "5", "6", "7", "8"]
# ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]

board[7][0] = "R"
def move(board):
    move = input("input move: ")

    
    
    piece = move[0]
    rank = int(move[1])
    file = int(move[2])
    if board[rank][file] != piece:
        return board
    match(piece):
        case "R":
            if int(move[3]) == int(move[1]) or int(move[4]) == int(move[2]):
                board[int(move[3])][int(move[4])] == move[1]
                board[int(move[1])][int(move[2])] == " "
                return board
            else:
                return board
        case "N":
            ...
        case "B":
            ...
        case "Q":
            ...
        case "K":
            ...

while True:
    for i in board:
        print(i)
    board = move(board)
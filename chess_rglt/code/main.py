r1 = ["br", "bh", "bb", "bq", "bk", "bb", "bh", "br"]
r2 = ["bp" for _ in range(8)]

r3to6 = ["  " for _ in range(8)]

r7 = ["wr", "wh", "wb", "wq", "wk", "wb", "wh", "wr"]
r8 = ["wp" for _ in range(8)]

board = []

board.append(r1)
board.append(r2)
for _ in range(4):
    board.append(r3to6)
board.append(r7)
board.append(r8)


for i in board:
    print(i)


import turtle

# ---------------- MAIN VARIABLE ----------------
SQUARE_SIZE = 64      # ändra till t.ex. 64 här
BOARD_SIZE = 8

BOARD_PIXELS = SQUARE_SIZE * BOARD_SIZE
SCREEN_PADDING = SQUARE_SIZE

# ---------------- SCREEN ----------------
screen = turtle.Screen()
screen.setup(
    width=BOARD_PIXELS + SCREEN_PADDING,
    height=BOARD_PIXELS + SCREEN_PADDING
)
screen.title("Chessboard")

# ---------------- TURTLE ----------------
t = turtle.Turtle()
t.speed(2)
t.pensize(1)

# ---------------- FUNCTIONS ----------------
def draw_square(color):
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(SQUARE_SIZE)
        t.left(90)
    t.end_fill()

def draw_board():
    start_x = -BOARD_PIXELS // 2
    start_y = -BOARD_PIXELS // 2

    t.penup()
    t.goto(start_x, start_y)
    t.setheading(0)
    t.pendown()

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = "white" if (row + col) % 2 == 0 else "black"
            draw_square(color)
            t.forward(SQUARE_SIZE)

        # nästa rad
        t.penup()
        t.goto(start_x, start_y + (row + 1) * SQUARE_SIZE)
        t.pendown()


def draw_piece(piece_distances, piece_angles, color, position):
    t.penup()
    t.goto(position)
    t.fillcolor(color)
    t.pendown()
    
    for i, j in enumerate(piece_distances):
        t.forward(i)
        t.left(piece_angles[j])
        
        
        
# ---------------- RUN ----------------





PAWN_DISTANCES = [
    36, 8, 3, 3, 3, 3, 3, 23]

PAWN_ANGLES = [
    90, 90, -90, 90, -90, 90, -90, 0]



def draw_piece(PIECE_DISTANCES, PIECE_ANGLES, position, color):
    t.penup()
    t.goto(position)
    t.setheading(0)
    t.fillcolor(color)
    t.pendown()
    t.begin_fill()

    for i in range(len(PIECE_DISTANCES)):
        t.forward(PIECE_DISTANCES[i])
        t.left(PIECE_ANGLES[i])

    t.end_fill()




t.penup()
t.goto(32, 32)
t.pendown()
t.left(180)

for _ in range(4):
    t.forward(64)
    t.left(90)

# for _ in range(4):
#     t.forward(48)
#     t.left(90)
    
draw_piece(PAWN_DISTANCES, PAWN_ANGLES, (-18, -24), "black")
















# draw_board()

screen.mainloop()

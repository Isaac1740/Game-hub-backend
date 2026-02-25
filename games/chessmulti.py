import random



# =========================
# Puzzle Boards
# =========================

puzzles = {
    "easy": [[
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]],
    "hard": [[
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]]
}

# =========================
# Game State
# =========================

board = []
turn = "white"
winner = None
difficulty = "easy"
game_mode = "pvp"

# =========================
# Game Control
# =========================

def load_game(diff="easy", mode="pvp"):
    global board, turn, winner, difficulty, game_mode
    difficulty = diff
    game_mode = mode
    board = [row[:] for row in puzzles[difficulty][0]]
    turn = "white"
    winner = None


def get_state():
    return {
        "board": board,
        "turn": turn,
        "winner": winner,
        "mode": game_mode
    }

# Initialize once
load_game()

# =========================
# Helpers
# =========================

def inside(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def enemy(piece, color):
    return piece.islower() if color == "white" else piece.isupper()


# =========================
# Move Generation
# =========================

def get_moves(piece, x, y, color):
    moves = []
    directions = []

    # Pawn
    if piece.lower() == 'p':
        d = -1 if color == 'white' else 1
        if inside(x+d, y) and board[x+d][y] == '.':
            moves.append((x+d, y))
        for dy in [-1, 1]:
            if inside(x+d, y+dy) and board[x+d][y+dy] != '.' and enemy(board[x+d][y+dy], color):
                moves.append((x+d, y+dy))

    # Rook
    elif piece.lower() == 'r':
        directions = [(-1,0),(1,0),(0,-1),(0,1)]

    # Bishop
    elif piece.lower() == 'b':
        directions = [(-1,-1),(-1,1),(1,-1),(1,1)]

    # Queen
    elif piece.lower() == 'q':
        directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

    # Knight
    elif piece.lower() == 'n':
        for dx,dy in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            tx,ty = x+dx, y+dy
            if inside(tx,ty) and (board[tx][ty]=='.' or enemy(board[tx][ty], color)):
                moves.append((tx,ty))

    # King
    elif piece.lower() == 'k':
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            tx,ty = x+dx, y+dy
            if inside(tx,ty) and (board[tx][ty]=='.' or enemy(board[tx][ty], color)):
                moves.append((tx,ty))

    # Sliding pieces
    for dx,dy in directions:
        tx,ty = x+dx, y+dy
        while inside(tx,ty):
            if board[tx][ty] == '.':
                moves.append((tx,ty))
            else:
                if enemy(board[tx][ty], color):
                    moves.append((tx,ty))
                break
            tx += dx
            ty += dy

    return moves

# =========================
# Game Actions
# =========================

def player_move(data):
    global turn, winner

    fx, fy = data["from"]
    tx, ty = data["to"]

    piece = board[fx][fy]

    if piece == '.':
        return {"error": "empty square"}, 400

    if turn == "white" and not piece.isupper():
        return {"error": "not your piece"}, 400

    if turn == "black" and not piece.islower():
        return {"error": "not your piece"}, 400

    if (tx, ty) not in get_moves(piece, fx, fy, turn):
        return {"error": "illegal move"}, 400

    board[tx][ty] = piece
    board[fx][fy] = '.'
    turn = "black" if turn == "white" else "white"

    return {"status": "ok", "turn": turn}, 200


def agent_move():
    global turn

    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j].islower():
                for tx,ty in get_moves(board[i][j], i, j, "black"):
                    moves.append((i,j,tx,ty))

    if not moves:
        return {"status": "stalemate"}

    fx,fy,tx,ty = random.choice(moves)
    board[tx][ty] = board[fx][fy]
    board[fx][fy] = '.'
    turn = "white"

    return {"status": "ok", "turn": "white"}

import os
import sys

#so u dont forget, [t]c means target [s]c means source
#checkmate logic does not work, #todo after submission
#https://github.com/KenzoSutanto/ChessPy--June-project- (will try to finish by end of this month, {probably})

turnsPlayed = 0

pieces = {"wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙",
          "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚", "bP": "♟"}

white_pieces = {"♖", "♘", "♗", "♕", "♔", "♙"}
black_pieces = {"♜", "♞", "♝", "♛", "♚", "♟"}


board = [
    [pieces["bR"], pieces["bN"], pieces["bB"], pieces["bQ"], pieces["bK"], pieces["bB"], pieces["bN"], pieces["bR"]],
    [pieces["bP"]]*8,
    ["*"]*8,
    ["*"]*8,
    ["*"]*8,
    ["*"]*8,
    [pieces["wP"]]*8,
    [pieces["wR"], pieces["wN"], pieces["wB"], pieces["wQ"], pieces["wK"], pieces["wB"], pieces["wN"], pieces["wR"]],
]


import sys

def main():
    global turnsPlayed
    while True:
        res = move_piece()
        if res == "mate":
            break  
        if not res:
            print("Please enter a valid move")
        else:
            turnsPlayed += 1

        print_board()
        print(f"{turnValidation()} to play")
        if input("Press [Enter] to continue, or type [Q] to quit: ").upper()=="Q":
            break
        os.system("clear")




def print_board():
    row_num = 8
    print("  A B C D E F G H")
    for row in board:
        line = f"{row_num}"
        for square in row:
            line += f" {square}"
        print(line)
        row_num -= 1


def move_core(r, c, tr, tc):
    board[tr][tc], board[r][c] = board[r][c], "*"


def move_piece():
    print_board()
    try:
        m = input("Enter a piece: ")

        current_player = turnValidation()
        was_in_check = check(current_player)
        suffix = ""

        if m[-1] in {"+", "#"}:
            suffix = m[-1]
            m = m[:-1]

        if len(m) == 2:
            tr, tc = 8 - int(m[1]), ord(m[0]) - 97
            valid = move_pawn(tr, tc, current_player)
        elif len(m) == 4 and m[1] == "x" and m[0].islower() and m[0] not in "NBRKQ":
            src_file = m[0]
            tr, tc = 8 - int(m[3]), ord(m[2]) - 97
            valid = capture_pawn(tr, tc, current_player, src_file)
        elif m[0] in "NBRKQ" and len(m) == 3:
            tr, tc = 8 - int(m[2]), ord(m[1]) - 97
            piece_func = {"N": move_knight, "B": move_bishop, "R": move_rook, "K": move_king, "Q": move_queen}[m[0]]
            valid = piece_func(tr, tc, current_player)
        elif m[0] in "NBRKQ" and len(m) == 4:
            tr, tc = 8 - int(m[3]), ord(m[2]) - 97
            piece_fun = {"N": capture_nkp, "B": capture_bishop, "R": capture_rook, "K": capture_nkp, "Q": capture_queen}[m[0]]
            valid = piece_fun(tr, tc, current_player)
        else:
            return False

        if not valid:
            return False
        if check(current_player):
            return False
        if was_in_check and check(current_player):
            return False

        enemy = "Black" if current_player == "White" else "White"
        if suffix == "+" and not check(enemy):
            return False


        if checkmate(enemy) == "mate":
            for i in range(8):
                board[i] = ["*"] * 8
            os.system("clear")
            print_board()
            print(f"Checkmate! {current_player} wins.")
            sys.exit(0)

        if suffix == "#" and not checkmate(enemy):
            return False

        return True

    except Exception:
        return False



def turnValidation():
    return "White" if turnsPlayed % 2 == 0 else "Black"


def move(r, c, offsets, sym):
    player_color = "White" if sym in white_pieces else "Black"
    for dr, dc in offsets:
        sr, sc = r + dr, c + dc
        if (
            0 <= sr < 8 and 0 <= sc < 8 and
            board[sr][sc] == sym and
            player_color == turnValidation()
        ):
            move_core(sr, sc, r, c)
            return True
    return False

def capture_pawn(tr, tc, color, src_file):
    sym = pieces["wP"] if color == "White" else pieces["bP"]
    enemy = black_pieces if color == "White" else white_pieces
    if board[tr][tc] not in enemy:
        return False
    sc = ord(src_file) - 97
    dr = 1 if color == "White" else -1
    sr = tr + dr
    if 0 <= sr < 8 and 0 <= sc < 8 and board[sr][sc] == sym and color == turnValidation():
        move_core(sr, sc, tr, tc)
        return True
    return False


def capture_nkp(tr, tc, offsets, sym):
    player_color = "White" if sym in white_pieces else "Black"
    enemy_set = black_pieces if player_color=="White" else white_pieces
    if board[tr][tc] not in enemy_set:
        return False
    for dr, dc in offsets:
        sr, sc = tr + dr, tc + dc
        if 0 <= sr < 8 and 0 <= sc < 8 and board[sr][sc] == sym and player_color == turnValidation(): #reverse search
            move_core(sr, sc, tr, tc)
            return True
    return False

def capture_qbr(tr, tc, offsets, sym):
    player_color = "White" if sym in white_pieces else "Black"
    enemy_set = black_pieces if player_color == "White" else white_pieces
    if board[tr][tc] not in enemy_set:
        return False
    for dr, dc in offsets:
        sr, sc = tr + dr, tc + dc
        while 0 <= sr < 8 and 0 <= sc < 8:
            if board[sr][sc] == sym and player_color == turnValidation():
                move_core(sr, sc, tr, tc)
                return True
            if board[sr][sc] != "*":
                break
            sr += dr
            sc += dc #reverse search with iteration because of the fly across the board thing
    return False

    

def move_qbr(r, c, offsets, sym):
    player_color = "White" if sym in white_pieces else "Black"
    for dr, dc in offsets:
        sr, sc = r + dr, c + dc
        while 0 <= sr < 8 and 0 <= sc < 8:
            if board[sr][sc] == sym:
                if player_color == turnValidation():
                    move_core(sr, sc, r, c)
                    return True
                else:
                    break
            if board[sr][sc] != "*":
                break
            sr += dr
            sc += dc
    return False

def capture_rook(r, c, color):
    sym = pieces["wR"] if color == "White" else pieces["bR"]
    return capture_qbr(r, c, [(-1, 0), (1, 0), (0, -1), (0, 1)], sym)


def capture_bishop(r, c, color):
    sym = pieces["wB"] if color == "White" else pieces["bB"]
    return capture_qbr(r, c, [(-1, -1), (-1, 1), (1, -1), (1, 1)], sym)

def capture_queen(r, c, color):
    sym = pieces["wQ"] if color == "White" else pieces["bQ"]
    return capture_qbr(r, c, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)], sym)

def capture_knight(tr, tc, color):
    sym = pieces["wN"] if color=="White" else pieces["bN"]
    offsets = [(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1)]
    return capture_nkp(tr, tc, offsets, sym)

def capture_king(tr, tc, color):
    sym = pieces["wK"] if color=="White" else pieces["bK"]
    offsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    return capture_nkp(tr, tc, offsets, sym)


def move_knight(r, c, color):
    sym = pieces["wN"] if color == "White" else pieces["bN"]
    return move(r, c, [(-2, -1), (-1, -2), (1, -2), (2, -1),
                       (2, 1), (1, 2), (-1, 2), (-2, 1)], sym)




def move_rook(r, c, color):
    sym = pieces["wR"] if color == "White" else pieces["bR"]
    return move_qbr(r, c, [(-1, 0), (1, 0), (0, -1), (0, 1)], sym)


def move_bishop(r, c, color):
    sym = pieces["wB"] if color == "White" else pieces["bB"]
    return move_qbr(r, c, [(-1, -1), (-1, 1), (1, -1), (1, 1)], sym)


def move_king(r, c, color):
    sym = pieces["wK"] if color == "White" else pieces["bK"]
    return move(r, c, [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1)], sym)


def move_queen(r, c, color):
    sym = pieces["wQ"] if color == "White" else pieces["bQ"]
    return move_qbr(r, c, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)], sym)


def move_pawn(tr, tc, color):
    sym = pieces["wP"] if color == "White" else pieces["bP"]
   
    if board[tr][tc] != "*":
        return False


    direction = -1 if color == "White" else 1


    sr = tr - direction
    if 0 <= sr < 8 and board[sr][tc] == sym:
        move_core(sr, tc, tr, tc)
        return True


    start = 6 if color == "White" else 1
    sr2 = tr - 2 * direction
    mid = tr - direction
    if (
        sr2 == start and
        board[sr2][tc] == sym and
        0 <= mid < 8 and
        board[mid][tc] == "*"
    ):
        move_core(sr2, tc, tr, tc)
        return True

    return False



def turnValidation():
    return "White" if turnsPlayed % 2 == 0 else "Black"


import sys

def checkmate(color):
    if not check(color):
        return False

    for sr in range(8):
        for sc in range(8):
            piece = board[sr][sc]
            if (color == "White" and piece in white_pieces) or (color == "Black" and piece in black_pieces):
                for tr in range(8):
                    for tc in range(8):
                        if sr == tr and sc == tc:
                            continue
                        target = board[tr][tc]
                        if color == "White" and target in white_pieces:
                            continue
                        if color == "Black" and target in black_pieces:
                            continue
                        if not attackable(sr, sc, tr, tc):
                            continue

                        moved_piece = board[sr][sc]
                        captured = board[tr][tc]
                        board[tr][tc] = moved_piece
                        board[sr][sc] = "*"

                        still_in_check = check(color)

                        board[sr][sc] = moved_piece
                        board[tr][tc] = captured

                        if not still_in_check:
                            return False

    return "mate"


def check(color):
    king = pieces["wK"] if color == "White" else pieces["bK"]
    opponent = "Black" if color == "White" else "White"

    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                king_pos = (r, c)
                break
        else:
            continue
        break

    for r in range(8):
        for c in range(8):
            if (opponent == "White" and board[r][c] in white_pieces) or \
               (opponent == "Black" and board[r][c] in black_pieces):
                if attackable(r, c, king_pos[0], king_pos[1]):
                    return True
    return False


def moveable(r, c, tr, tc, offsets, sym):
    for dr, dc in offsets:
        sr, sc = r + dr, c + dc
        if sr == tr and sc == tc and 0 <= sr < 8 and 0 <= sc < 8 and board[r][c] == sym:
            return True
    return False


def moveable_qbr(r, c, tr, tc, offsets, sym):
    for dr, dc in offsets:
        sr, sc = r + dr, c + dc
        while 0 <= sr < 8 and 0 <= sc < 8:
            if sr == tr and sc == tc and board[r][c] == sym:
                return True
            if board[sr][sc] != "*":
                break
            sr += dr
            sc += dc
    return False


def attackable(sr, sc, tr, tc):
    piece = board[sr][sc]
    if piece == pieces["wN"] or piece == pieces["bN"]:
        return moveable(sr, sc, tr, tc, [(-2, -1), (-1, -2), (1, -2), (2, -1),
                                         (2, 1), (1, 2), (-1, 2), (-2, 1)], piece)
    elif piece == pieces["wK"] or piece == pieces["bK"]:
        return moveable(sr, sc, tr, tc, [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                                         (0, 1), (1, -1), (1, 0), (1, 1)], piece)
    elif piece == pieces["wR"] or piece == pieces["bR"]:
        return moveable_qbr(sr, sc, tr, tc, [(-1, 0), (1, 0), (0, -1), (0, 1)], piece)
    elif piece == pieces["wB"] or piece == pieces["bB"]:
        return moveable_qbr(sr, sc, tr, tc, [(-1, -1), (-1, 1), (1, -1), (1, 1)], piece)
    elif piece == pieces["wQ"] or piece == pieces["bQ"]:
        return moveable_qbr(sr, sc, tr, tc, [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                                             (0, 1), (1, -1), (1, 0), (1, 1)], piece)
    elif piece == pieces["wP"]:
        return (sr - 1 == tr) and (abs(sc - tc) == 1)
    elif piece == pieces["bP"]:
        return (sr + 1 == tr) and (abs(sc - tc) == 1)
    return False

main()

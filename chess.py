turnsPlayed = 0
def main():
    global turnsPlayed
    quit = "no"
    while quit != "Q":
        result = move_piece()
        if result != "invalid":
            turnsPlayed += 1
        else:
            print("Please enter a valid move")
        quit = input("Press [Enter] or any key, else type [Q] to quit").upper()


pieces = {"wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK":"♔", "wP": "♙",
          "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚" ,"bP": "♟"}

white_pieces = {"♙", "♖", "♘", "♗", "♕", "♔"}
black_pieces = {"♟", "♜", "♞", "♝", "♛", "♚"}

board = [
    [pieces["bR"], pieces["bN"], pieces["bB"], pieces["bQ"], pieces["bK"], pieces["bB"], pieces["bN"], pieces["bR"]],
    [pieces["bP"], pieces["bP"], pieces["bP"], pieces["bP"], pieces["bP"], pieces["bP"], pieces["bP"], pieces["bP"]],
    ["*", "*", "*", "*", "*", "*", "*", "*"],
    ["*", "*", "*", "*", "*", "*", "*", "*"],
    ["*", "*", "*", "*", "*", "*", "*", "*"],
    ["*", "*", "*", "*", "*", "*", "*", "*"],
    [pieces["wP"], pieces["wP"], pieces["wP"], pieces["wP"], pieces["wP"], pieces["wP"], pieces["wP"], pieces["wP"]],
    [pieces["wR"], pieces["wN"], pieces["wB"], pieces["wQ"], pieces["wK"], pieces["wB"], pieces["wN"], pieces["wR"]],
] #Public var board and piece dictionary

def print_board():
    row_num =8  # Adding from 8 down to 1 because white is at the bottom now
    cols = "  A B C D E F G H"
    print(cols)
    for row in board:
        line = f"{row_num}"
        for square in row:
            line += f" {square}"
        print(line)
        row_num -= 1

def move_piece_core(row,col,endrow,endcol):
    board[endrow][endcol] = board[row][col] 
    board[row][col] = "*"

def move_piece():
    print_board()
    try:
        move = input("Enter a piece: ")
        print(move)
        if len(move) == 2: #pawn move
            endcol = ord(move[0]) - 97  # getting the column, e in e7
            endrow = 8 - int(move[1])    # getting the row, flipped
            return move_pawn(endrow,endcol)
        elif move[0] == 'N':
            endcol = ord(move[1]) - 97  # getting the column, e in e7
            endrow = 8 - int(move[2]) 
            return move_knight(endrow,endcol)
        else:
            return "invalid"
        print_board()
    except:
        return "invalid"

def move_knight(tgt_rw, tgt_col):


    knight_offsets = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
    try:
        knightPos = []
        if turnValidation() == "White":
            for dr,dc in knight_offsets:
                r,c = tgt_rw + dr, tgt_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if (board[r][c] == pieces["wN"]):
                        move_piece_core(r,c,tgt_rw,tgt_col)
                        return "Valid" 
            return "invalid"
                        
        elif turnValidation() == "Black":
            for dr,dc in knight_offsets:
                r,c = tgt_rw + dr, tgt_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if (board[r][c] == pieces["bN"]):
                        move_piece_core(r,c,tgt_rw,tgt_col)
                        return "Valid" 
            return "invalid"

       
    except:
        return "invalid"

def move_pawn(tgt_rw, tgt_col):
    try:
        if turnValidation() == "White" and turnsPlayed == 0:
            pawn_offsets = [(1,0),(2,0)]
            pawnPos = []    
            for dr,dc in pawn_offsets:
                r,c = tgt_rw + dr, tgt_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if (board[r][c] == pieces["wP"]):
                        pawnPos.append((r, c))
                        row,col = pawnPos[0]
                        move_piece_core(row,col,tgt_rw,tgt_col)
                        return "Valid"
            return "invalid"
        elif turnValidation() == "White":
            pawn_offsets = [(1,0)]
            pawnPos = []    
            for dr,dc in pawn_offsets:
                r,c = tgt_rw + dr, tgt_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if (board[r][c] == pieces["wP"]):
                        pawnPos.append((r, c))
                        row,col = pawnPos[0]
                        move_piece_core(row,col,tgt_rw,tgt_col)
                        return "Valid"
            return "invalid"

        elif turnValidation() == "Black" and turnsPlayed == 1:
            pawn_offsets = [(-1,0),(-2,0)]
            pawnPos = []
            for dr,dc in pawn_offsets:
                r,c = tgt_rw + dr, tgt_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if (board[r][c] == pieces["bP"]):
                        pawnPos.append((r, c))
                        row,col = pawnPos[0]
                        move_piece_core(row,col,tgt_rw,tgt_col)
                        return "Valid"
            return "invalid"
        elif turnValidation() == "Black":
            pawn_offsets = [(-1,0)]
            pawnPos = []
            for dr,dc in pawn_offsets:
                r,c = tgt_rw + dr, tgt_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if (board[r][c] == pieces["bP"]):
                        pawnPos.append((r, c))
                        row,col = pawnPos[0]
                        move_piece_core(row,col,tgt_rw,tgt_col)
                        return "Valid"
            return "invalid"
    except:
        return "invalid"

def move_king(tgt_rw, tgt_col):
    king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    kingPos = []
    for dr,dc in king_offsets:
        r,c = tgt_rw + dr,tgt_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if (board[r][c] == (pieces["bK"] or pieces["wK"])):
                kingPos.append((r,c))
                row,col = kingPos = [0]
                move_piece_core(row,col,tgt_rw,tgt_col)
                return "Valid"
    return "invalid"






def turnValidation():
    if (turnsPlayed % 2 != 0):
        return "Black"
    else:
        return "White"
    

main()
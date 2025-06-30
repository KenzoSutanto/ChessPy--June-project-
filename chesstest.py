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

def get_piece():
    location = input("Piece Location: ")
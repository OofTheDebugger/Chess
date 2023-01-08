import chess

board = chess.Board()
square_mapping = {name: index for index, name in enumerate(chess.SQUARE_NAMES)}

def parse_move(move_str):
    move_str = move_str.lower()
    try:
        # Try parsing the move as Long Algebraic Notation (LAN)
        if len(move_str) < 5:
            raise ValueError("invalid lan: move string is too short")
        source_square = move_str[1:3]
        dest_square = move_str[-2:]
        if len(move_str) == 6:
            promotion = move_str[3]
        else:
            promotion = ""
        # Create the UCI string representation of the move
        uci_str = source_square + dest_square + promotion
        # Create a move object from the UCI string
        return chess.Move.from_uci(uci_str)
    except ValueError:
        # If that fails, try parsing the move as Coordinate Notation (CN)
        try:
            return chess.Move.from_uci(move_str)
        except ValueError:
            # If that also fails, try parsing the move as Standard Algebraic Notation (SAN)
            if move_str[0] == "q":
                # If the move starts with 'q', assume it is a queen promotion
                # and add the source square to the move string
                for move in board.legal_moves:
                    if move.promotion and move.to_square == chess.SQUARE_NAMES.index(move_str[1:]):
                        move_str = chess.SQUARE_NAMES[move.from_square] + move_str[1:]
                        break
            return board.parse_san(move_str)



while True:
    to_square = input("Enter a move in one of the following formats: Standard Algebraic Notation (e.g. 'Nf3'), Coordinate Notation (e.g. 'g1f3'), Long Algebraic Notation (e.g. 'Ng1f3'): ")
    try:
        move = parse_move(to_square)
    except ValueError as e:
        print(e)
        continue
    board.push(move)
    print(board)

    result = board.result()
    if result != "*":
        print(result)
        break

    if not board.legal_moves:
        print("Draw")
        break

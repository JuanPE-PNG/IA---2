from pieces import create_initial_board, Piece

class Board:
    def __init__(self):
        self.board1 = create_initial_board()
        
        self.board2 = [[None for _ in range(8)] for _ in range(8)]
        
        self.current_player = 'white'
        
        self.move_history = []
        
        self.game_over = False
        self.winner = None

    def get_piece(self, position, board_number):
        """
        Obtener pieza en una posición específica de un tablero
        """
        x, y = position
        board = self.board1 if board_number == 1 else self.board2
        return board[x][y]

    def is_valid_move(self, start, end, board_number):
        """
        Verificar si un movimiento es válido
        """
        board = self.board1 if board_number == 1 else self.board2
        
        piece = board[start[0]][start[1]]
        
        if piece is None:
            return False
        
        if piece.color != self.current_player:
            return False
        
        possible_moves = piece.get_possible_moves(board, start)
        
        if end not in possible_moves:
            return False
        
        other_board = self.board2 if board_number == 1 else self.board1
        if other_board[end[0]][end[1]] is not None:
            return False
        
        return True

    def move_piece(self, start, end, board_number):
        """
        Mover una pieza de una posición a otra en un tablero específico
        """
        if not self.is_valid_move(start, end, board_number):
            raise ValueError("Movimiento inválido")
        
        board = self.board1 if board_number == 1 else self.board2
        
        piece = board[start[0]][start[1]]
        board[start[0]][start[1]] = None
        board[end[0]][end[1]] = piece
        
        piece.has_moved = True
        
        self.move_history.append({
            'piece': piece,
            'start': start,
            'end': end,
            'board_number': board_number
        })
        
        target_board_number = 2 if board_number == 1 else 1
        self._transfer_to_other_board(end, target_board_number)
        
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        self._check_game_status()
        
        return True

    def _transfer_to_other_board(self, position, target_board_number):
        """
        Transferir una pieza a la misma posición en el otro tablero
        """
        x, y = position
        source_board = self.board1 if target_board_number == 2 else self.board2
        target_board = self.board2 if target_board_number == 2 else self.board1

        if target_board[x][y] is None:
            piece = source_board[x][y]
            source_board[x][y] = None
            target_board[x][y] = piece

    def _check_game_status(self):
        """
        Verificar si el juego ha terminado (jaque mate, tablas, etc.)
        """
        pass

    def undo_last_move(self):
        """
        Deshacer el último movimiento
        """
        if not self.move_history:
            return False
        
        last_move = self.move_history.pop()
        
        board = self.board1 if last_move['board_number'] == 1 else self.board2
        
        board[last_move['start'][0]][last_move['start'][1]] = last_move['piece']
        board[last_move['end'][0]][last_move['end'][1]] = None
        
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        return True

    def print_board(self, board_number):
        """
        Imprimir el estado de un tablero
        """
        board = self.board1 if board_number == 1 else self.board2
        
        print(f"Tablero {board_number}")
        for row in board:
            row_str = []
            for piece in row:
                if piece is None:
                    row_str.append('.')
                else:
                    row_str.append(f"{piece.color[0]}{piece.name[0]}")
            print(' '.join(row_str))
        print(f"Turno actual: {self.current_player}")

def main():
    board = Board()
    
    board.print_board(1)
    board.print_board(2)
    
    try:
        board.move_piece((6, 3), (4, 3), 1)
        board.print_board(1)
        board.print_board(2)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

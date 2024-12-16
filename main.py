import tkinter as tk
from tkinter import messagebox
from board import Board
from gui import ChessGUI
from ai import ChessAI

class AliceSuicideChess:
    def __init__(self):
        # Initialize the game board
        self.board = Board()
        
        # Game rules configuration
        self.suicide_mode = True  # Suicide chess rules
        self.alice_mode = True   # Two-board chess rules
        
        # Player and AI configuration
        self.current_player = 'white'
        self.ai_player = 'black'
        
        # Game state tracking
        self.game_over = False
        self.winner = None
    
    def check_game_over(self):
        """
        Check if the game is over based on suicide chess rules
        """
        if not self.suicide_mode:
            return False
        
        # Check if the current player has no valid moves or no pieces left
        board_to_check = self.board.board1 if self.current_player == 'white' else self.board.board2
        
        # Count pieces and movable pieces
        pieces_count = 0
        movable_pieces = 0
        
        for x in range(8):
            for y in range(8):
                piece = board_to_check[x][y]
                if piece and piece.color == self.current_player:
                    pieces_count += 1
                    
                    # Check if this piece has any possible moves
                    moves = piece.get_possible_moves(board_to_check, (x, y))
                    if moves:
                        movable_pieces += 1
        
        # In suicide chess, you MUST capture if possible
        # So if there are no moves, you've lost
        if movable_pieces == 0:
            self.game_over = True
            self.winner = 'black' if self.current_player == 'white' else 'white'
            return True
        
        return False
    
    def is_forced_capture(self, board, color):
        """
        Determine if there are mandatory captures in suicide chess
        """
        for x in range(8):
            for y in range(8):
                piece = board[x][y]
                if piece and piece.color == color:
                    moves = piece.get_possible_moves(board, (x, y))
                    for move in moves:
                        # Check if this move is a capture
                        if board[move[0]][move[1]] is not None and board[move[0]][move[1]].color != color:
                            return True
        return False
    
    def validate_move(self, start, end, board_num):
        """
        Validate move according to suicide chess and Alice's chess rules
        """
        board = self.board.board1 if board_num == 1 else self.board.board2
        piece = board[start[0]][start[1]]
        
        # Suicide chess capture rule
        if self.suicide_mode:
            # If captures are possible, player MUST capture
            if self.is_forced_capture(board, piece.color):
                capture_moves = [
                    move for move in piece.get_possible_moves(board, start) 
                    if board[move[0]][move[1]] is not None and board[move[0]][move[1]].color != piece.color
                ]
                
                if capture_moves:
                    # Player MUST choose a capture move
                    if end not in capture_moves:
                        raise ValueError("In Suicide Chess, you must capture if possible!")
        
        return True
    
    def start_game(self):
        """
        Start the game with GUI
        """
        # Create the GUI
        self.gui = ChessGUI(self.board)
        
        # Override some GUI methods to incorporate our game rules
        original_move_method = self.gui.on_square_click
        def custom_move_method(event, board_num):
            # Custom move validation
            try:
                # Si ya hay una pieza seleccionada
                if self.gui.selected_piece:
                    start = self.gui.selected_piece
                    end = (event.y // self.gui.square_size, event.x // self.gui.square_size)
                    
                    # Validate move according to our custom rules
                    board = self.board.board1 if board_num == 1 else self.board.board2
                    piece = board[start[0]][start[1]]
                    
                    if piece and piece.color == self.current_player:
                        self.validate_move(start, end, board_num)
                
                # Call original move method
                original_move_method(event, board_num)
                
                # Check game over after move
                if self.check_game_over():
                    messagebox.showinfo("Game Over", f"Winner: {self.winner}")
                
            except ValueError as e:
                messagebox.showerror("Invalid Move", str(e))
        
        self.gui.on_square_click = custom_move_method
        
        # Run the game
        self.gui.run()

def main():
    game = AliceSuicideChess()
    game.start_game()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox
from board import Board
from gui import ChessGUI
from ai import ChessAI

class AliceSuicideChess:
    def __init__(self):

        self.board = Board()
        

        self.suicide_mode = True  
        self.alice_mode = True   
        
        self.current_player = 'white'
        self.ai_player = 'black'
        
        self.game_over = False
        self.winner = None
    
    def check_game_over(self):
        """
        Check if the game is over based on suicide chess rules
        """
        if not self.suicide_mode:
            return False
        
        board_to_check = self.board.board1 if self.current_player == 'white' else self.board.board2
        
        pieces_count = 0
        movable_pieces = 0
        
        for x in range(8):
            for y in range(8):
                piece = board_to_check[x][y]
                if piece and piece.color == self.current_player:
                    pieces_count += 1
                    
                    moves = piece.get_possible_moves(board_to_check, (x, y))
                    if moves:
                        movable_pieces += 1
        

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
                        if board[move[0]][move[1]] is not None and board[move[0]][move[1]].color != color:
                            return True
        return False
    
    def validate_move(self, start, end, board_num):
        """
        Validate move according to suicide chess and Alice's chess rules
        """
        board = self.board.board1 if board_num == 1 else self.board.board2
        piece = board[start[0]][start[1]]
        
        if self.suicide_mode:
            if self.is_forced_capture(board, piece.color):
                capture_moves = [
                    move for move in piece.get_possible_moves(board, start) 
                    if board[move[0]][move[1]] is not None and board[move[0]][move[1]].color != piece.color
                ]
                
                if capture_moves:
                    if end not in capture_moves:
                        raise ValueError("In Suicide Chess, you must capture if possible!")
        
        return True
    
    def start_game(self):
        """
        Start the game with GUI
        """
        self.gui = ChessGUI(self.board)
        
        original_move_method = self.gui.on_square_click
        def custom_move_method(event, board_num):
            try:
                if self.gui.selected_piece:
                    start = self.gui.selected_piece
                    end = (event.y // self.gui.square_size, event.x // self.gui.square_size)
                    
                    board = self.board.board1 if board_num == 1 else self.board.board2
                    piece = board[start[0]][start[1]]
                    
                    if piece and piece.color == self.current_player:
                        self.validate_move(start, end, board_num)
                

                original_move_method(event, board_num)
                

                if self.check_game_over():
                    messagebox.showinfo("Game Over", f"Winner: {self.winner}")
                
            except ValueError as e:
                messagebox.showerror("Invalid Move", str(e))
        
        self.gui.on_square_click = custom_move_method
        
        self.gui.run()

def main():
    game = AliceSuicideChess()
    game.start_game()

if __name__ == "__main__":
    main()
import random
import copy

class ChessAI:
    def __init__(self, board_instance, color):
        self.board_instance = board_instance
        self.color = color
        # Adjusted piece values to prioritize captures
        self.piece_values = {
            'Pawn': 10,
            'Knight': 30,
            'Bishop': 30,
            'Rook': 50,
            'Queen': 90,
            'King': 900
        }

    def get_all_possible_moves(self, board1, board2, color):
        """
        Get all possible moves for a color, prioritizing captures
        """
        moves = []
        capture_moves = []

        for x in range(8):
            for y in range(8):
                piece = board1[x][y]
                if piece and piece.color == color:
                    # Get possible moves for the piece
                    piece_moves = piece.get_possible_moves(board1, (x, y))
                    
                    for move in piece_moves:
                        # Check if the move is a capture on either board
                        dest_board1 = board1[move[0]][move[1]]
                        dest_board2 = board2[move[0]][move[1]]

                        # Skip moves if destination on the opposite board is blocked
                        if dest_board2:
                            continue
                        
                        # Prioritize captures
                        if dest_board1:
                            capture_moves.append((x, y, move, 1))
                            continue
                        
                        # Regular moves
                        moves.append((x, y, move, 1))

                        # Add cross-board moves if target is free
                        if not dest_board2:
                            cross_board_move = (x, y, move, 2)
                            moves.append(cross_board_move)
        
        # Always prioritize capture moves
        return capture_moves if capture_moves else moves

    def evaluate_board(self, board1, board2):
        """
        Evaluate board state with suicidal chess rules
        """
        score = 0
        piece_count = {
            self.color: 0,
            'white' if self.color == 'black' else 'black': 0
        }

        for board in [board1, board2]:
            for x in range(8):
                for y in range(8):
                    piece = board[x][y]
                    if piece:
                        # Count pieces
                        piece_count[piece.color] += 1
                        
                        # Value pieces
                        value = self.piece_values[piece.name]
                        score += value if piece.color == self.color else -value
        
        # Favor fewer pieces in suicidal chess
        score += (piece_count['white' if self.color == 'black' else 'black'] - 
                  piece_count[self.color]) * 50
        
        return score

    def minimax(self, board1, board2, depth, alpha, beta, maximizing_player):
        """
        Minimax with alpha-beta pruning for Alice Chess with suicidal elements
        """
        current_color = self.color if maximizing_player else ('white' if self.color == 'black' else 'black')
        
        if depth == 0:
            return self.evaluate_board(board1, board2)
        
        possible_moves = self.get_all_possible_moves(board1, board2, current_color)
        
        if not possible_moves:
            return self.evaluate_board(board1, board2)
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                board1_copy = copy.deepcopy(board1)
                board2_copy = copy.deepcopy(board2)
                
                start = (move[0], move[1])
                end = (move[2][0], move[2][1])
                board_source = board1_copy if move[3] == 1 else board2_copy
                board_dest = board2_copy if move[3] == 1 else board1_copy
                
                # Check for captures
                if board_dest[end[0]][end[1]] is not None:
                    board_dest[end[0]][end[1]] = None
                
                # Move piece
                piece = board_source[start[0]][start[1]]
                board_source[start[0]][start[1]] = None
                board_dest[end[0]][end[1]] = piece
                
                eval = self.minimax(board1_copy, board2_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                
                if beta <= alpha:
                    break
            
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                board1_copy = copy.deepcopy(board1)
                board2_copy = copy.deepcopy(board2)
                
                start = (move[0], move[1])
                end = (move[2][0], move[2][1])
                board_source = board1_copy if move[3] == 1 else board2_copy
                board_dest = board2_copy if move[3] == 1 else board1_copy
                
                # Check for captures
                if board_dest[end[0]][end[1]] is not None:
                    board_dest[end[0]][end[1]] = None
                
                # Move piece
                piece = board_source[start[0]][start[1]]
                board_source[start[0]][start[1]] = None
                board_dest[end[0]][end[1]] = piece
                
                eval = self.minimax(board1_copy, board2_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                
                if beta <= alpha:
                    break
            
            return min_eval

    def choose_best_move(self, depth=3):
        """
        Choose the best move for Alice Chess with suicidal elements
        """
        board1 = self.board_instance.board1
        board2 = self.board_instance.board2
        
        possible_moves = self.get_all_possible_moves(board1, board2, self.color)
        
        if not possible_moves:
            return None
        
        best_move = None
        best_value = float('-inf')
        
        # Shuffle moves to add some randomness if multiple moves have similar values
        random.shuffle(possible_moves)
        
        for move in possible_moves:
            board1_copy = copy.deepcopy(board1)
            board2_copy = copy.deepcopy(board2)
            
            start = (move[0], move[1])
            end = (move[2][0], move[2][1])
            board_source = board1_copy if move[3] == 1 else board2_copy
            board_dest = board2_copy if move[3] == 1 else board1_copy
            
            # Check for captures
            if board_dest[end[0]][end[1]] is not None:
                board_dest[end[0]][end[1]] = None
            
            # Move piece
            piece = board_source[start[0]][start[1]]
            board_source[start[0]][start[1]] = None
            board_dest[end[0]][end[1]] = piece
            
            # Evaluate move
            move_value = self.minimax(board1_copy, board2_copy, depth - 1, float('-inf'), float('inf'), False)
            
            # Update best move
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        return best_move

def main():
    from board import Board
    
    # Create board
    board_instance = Board()
    
    # Create AI for black, passing entire board instance
    ai = ChessAI(board_instance, 'black')
    
    # Get best move
    best_move = ai.choose_best_move()
    
    if best_move:
        print("Best move found:")
        print(f"From: ({best_move[0]}, {best_move[1]})")
        print(f"To: ({best_move[2][0]}, {best_move[2][1]})")
        print(f"On board: {best_move[3]}")
    else:
        print("No possible moves")

if __name__ == "__main__":
    main()

import copy

class Piece:
    def __init__(self, color, name):
        self.color = color 
        self.name = name
        self.has_moved = False 

    def __repr__(self):
        return f"{self.color} {self.name}"

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'Pawn')
        self.direction = -1 if color == 'white' else 1

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        forward_move = (x + self.direction, y)
        if self._is_valid_move(board, forward_move):
            moves.append(forward_move)
        
        if not self.has_moved:
            double_forward_move = (x + 2 * self.direction, y)
            if self._is_valid_move(board, double_forward_move):
                moves.append(double_forward_move)
        
        capture_moves = [
            (x + self.direction, y - 1),
            (x + self.direction, y + 1)
        ]
        for move in capture_moves:
            if self._is_valid_capture(board, move):
                moves.append(move)
        
        return moves

    def _is_valid_move(self, board, move):
        x, y = move
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        
        return board[x][y] is None

    def _is_valid_capture(self, board, move):
        x, y = move
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        
        piece = board[x][y]
        return piece is not None and piece.color != self.color

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'Rook')

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        directions = [
            (0, 1),   
            (0, -1),  
            (1, 0),  
            (-1, 0)  
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                else:
                    if board[new_x][new_y].color != self.color:
                        moves.append((new_x, new_y))
                    break
                
                new_x += dx
                new_y += dy
        
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'Knight')

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        knight_moves = [
            (x+2, y+1), (x+2, y-1),
            (x-2, y+1), (x-2, y-1),
            (x+1, y+2), (x+1, y-2),
            (x-1, y+2), (x-1, y-2)
        ]
        
        for move in knight_moves:
            nx, ny = move
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board[nx][ny]
                if piece is None or piece.color != self.color:
                    moves.append(move)
        
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'Bishop')

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        directions = [
            (1, 1),  
            (1, -1), 
            (-1, 1),  
            (-1, -1)  
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                else:
                    if board[new_x][new_y].color != self.color:
                        moves.append((new_x, new_y))
                    break
                
                new_x += dx
                new_y += dy
        
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Queen')

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        directions = [
            (0, 1),   
            (0, -1),  
            (1, 0),   
            (-1, 0),  
            (1, 1),   
            (1, -1),  
            (-1, 1),  
            (-1, -1)  
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                else:
                    if board[new_x][new_y].color != self.color:
                        moves.append((new_x, new_y))
                    break
                
                new_x += dx
                new_y += dy
        
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'King')

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        king_moves = [
            (x+1, y), (x-1, y),
            (x, y+1), (x, y-1),
            (x+1, y+1), (x+1, y-1),
            (x-1, y+1), (x-1, y-1)
        ]
        
        for move in king_moves:
            nx, ny = move
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board[nx][ny]
                if piece is None or piece.color != self.color:
                    moves.append(move)
        
        
        return moves

def create_initial_board():
    board = [[None for _ in range(8)] for _ in range(8)]
    
    for y in range(8):
        board[1][y] = Pawn('black')
        board[6][y] = Pawn('white')
    
    board[0][0] = Rook('black')
    board[0][7] = Rook('black')
    board[7][0] = Rook('white')
    board[7][7] = Rook('white')
    
    board[0][1] = Knight('black')
    board[0][6] = Knight('black')
    board[7][1] = Knight('white')
    board[7][6] = Knight('white')
    
    board[0][2] = Bishop('black')
    board[0][5] = Bishop('black')
    board[7][2] = Bishop('white')
    board[7][5] = Bishop('white')
    
    board[0][3] = Queen('black')
    board[7][3] = Queen('white')
    
    board[0][4] = King('black')
    board[7][4] = King('white')
    
    return board

board = create_initial_board()
print("Tablero de ajedrez inicializado")
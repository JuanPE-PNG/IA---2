import copy

class Piece:
    def __init__(self, color, name):
        self.color = color  # 'white' o 'black'
        self.name = name
        self.has_moved = False  # Para usar en movimientos especiales como enroque o peón

    def __repr__(self):
        return f"{self.color} {self.name}"

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'Pawn')
        # Dirección de movimiento depende del color
        self.direction = -1 if color == 'white' else 1

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        # Movimiento estándar de un cuadro hacia adelante
        forward_move = (x + self.direction, y)
        if self._is_valid_move(board, forward_move):
            moves.append(forward_move)
        
        # Primer movimiento puede ser de dos cuadros
        if not self.has_moved:
            double_forward_move = (x + 2 * self.direction, y)
            if self._is_valid_move(board, double_forward_move):
                moves.append(double_forward_move)
        
        # Capturas diagonales
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
        # Verificar límites del tablero
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        
        # Casilla debe estar vacía
        return board[x][y] is None

    def _is_valid_capture(self, board, move):
        x, y = move
        # Verificar límites del tablero
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        
        # Debe haber una pieza de color diferente
        piece = board[x][y]
        return piece is not None and piece.color != self.color

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'Rook')

    def get_possible_moves(self, board, current_position):
        moves = []
        x, y = current_position
        
        # Movimientos horizontales y verticales
        directions = [
            (0, 1),   # Derecha
            (0, -1),  # Izquierda
            (1, 0),   # Abajo
            (-1, 0)   # Arriba
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Continuar en esa dirección hasta encontrar un obstáculo
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                else:
                    # Si hay una pieza, verificar si es captura
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
        
        # Movimientos de caballo (L)
        knight_moves = [
            (x+2, y+1), (x+2, y-1),
            (x-2, y+1), (x-2, y-1),
            (x+1, y+2), (x+1, y-2),
            (x-1, y+2), (x-1, y-2)
        ]
        
        for move in knight_moves:
            nx, ny = move
            # Verificar límites y condiciones de movimiento
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
        
        # Direcciones diagonales
        directions = [
            (1, 1),   # Abajo-derecha
            (1, -1),  # Abajo-izquierda
            (-1, 1),  # Arriba-derecha
            (-1, -1)  # Arriba-izquierda
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Continuar en esa dirección diagonal
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                else:
                    # Si hay una pieza, verificar si es captura
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
        
        # Combinación de movimientos de torre y alfil
        directions = [
            (0, 1),   # Derecha
            (0, -1),  # Izquierda
            (1, 0),   # Abajo
            (-1, 0),  # Arriba
            (1, 1),   # Abajo-derecha
            (1, -1),  # Abajo-izquierda
            (-1, 1),  # Arriba-derecha
            (-1, -1)  # Arriba-izquierda
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Continuar en esa dirección
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                else:
                    # Si hay una pieza, verificar si es captura
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
        
        # Movimientos en todas las direcciones, un cuadro
        king_moves = [
            (x+1, y), (x-1, y),
            (x, y+1), (x, y-1),
            (x+1, y+1), (x+1, y-1),
            (x-1, y+1), (x-1, y-1)
        ]
        
        for move in king_moves:
            nx, ny = move
            # Verificar límites y condiciones de movimiento
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board[nx][ny]
                if piece is None or piece.color != self.color:
                    moves.append(move)
        
        # Aquí podrías agregar lógica de enroque en futuras versiones
        
        return moves

def create_initial_board():
    # Crear tablero inicial
    board = [[None for _ in range(8)] for _ in range(8)]
    
    # Peones
    for y in range(8):
        board[1][y] = Pawn('black')
        board[6][y] = Pawn('white')
    
    # Torres
    board[0][0] = Rook('black')
    board[0][7] = Rook('black')
    board[7][0] = Rook('white')
    board[7][7] = Rook('white')
    
    # Caballos
    board[0][1] = Knight('black')
    board[0][6] = Knight('black')
    board[7][1] = Knight('white')
    board[7][6] = Knight('white')
    
    # Alfiles
    board[0][2] = Bishop('black')
    board[0][5] = Bishop('black')
    board[7][2] = Bishop('white')
    board[7][5] = Bishop('white')
    
    # Reinas
    board[0][3] = Queen('black')
    board[7][3] = Queen('white')
    
    # Reyes
    board[0][4] = King('black')
    board[7][4] = King('white')
    
    return board

# Ejemplo de uso
board = create_initial_board()
print("Tablero de ajedrez inicializado")
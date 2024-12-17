import tkinter as tk
from tkinter import messagebox
import os

class ChessGUI:
    def __init__(self, board):
        self.board = board
        self.selected_piece = None
        self.selected_board = None
        
        self.window = tk.Tk()
        self.window.title("Ajedrez de Alicia")
        
        self.square_size = 70
        self.board_padding = 20
        
        self.create_board_frames()
        
        self.create_control_buttons()

    def create_board_frames(self):
        """Crear frames para los dos tableros"""
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(padx=10, pady=10)
        
        self.board_frames = []
        for board_num in [1, 2]:
            board_frame = tk.Frame(self.main_frame, relief=tk.RAISED, borderwidth=2)
            board_frame.grid(row=0, column=board_num-1, padx=10)
            
            label = tk.Label(board_frame, text=f"Tablero {board_num}")
            label.pack()
            
            canvas = tk.Canvas(
                board_frame, 
                width=self.square_size * 8, 
                height=self.square_size * 8
            )
            canvas.pack()
            
            self.draw_board(canvas, board_num)
            
            canvas.bind("<Button-1>", lambda e, bn=board_num: self.on_square_click(e, bn))
            
            self.board_frames.append({
                'frame': board_frame,
                'canvas': canvas
            })

    def draw_board(self, canvas, board_num):
        """Dibujar tablero de ajedrez"""
        canvas.delete("all")
        board = self.board.board1 if board_num == 1 else self.board.board2
        
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                color = "white" if (row + col) % 2 == 0 else "gray"
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                
                piece = board[row][col]
                if piece:
                    piece_text = self.get_piece_initials(piece)
                    canvas.create_text(
                        x1 + self.square_size // 2, 
                        y1 + self.square_size // 2, 
                        text=piece_text, 
                        font=("Arial", 24)
                    )

    def get_piece_initials(self, piece):
        """Obtener iniciales de la pieza con el color"""
        color_initial = piece.color[0].upper() 
        piece_initial = piece.name[0].upper()  
        return f"{piece_initial}{color_initial}"

    def create_control_buttons(self):
        """Crear botones de control"""
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        


        ai_btn = tk.Button(
            button_frame, 
            text="Mover IA", 
            command=self.make_ai_move
        )
        ai_btn.pack(side=tk.LEFT, padx=5)

    def on_square_click(self, event, board_num):
        """Manejar clics en el tablero"""
        col = event.x // self.square_size
        row = event.y // self.square_size
        
        board = self.board.board1 if board_num == 1 else self.board.board2
        
        if not self.selected_piece:
            piece = board[row][col]
            if piece and piece.color == self.board.current_player:
                self.selected_piece = (row, col)
                self.selected_board = board_num
                canvas = self.board_frames[board_num-1]['canvas']
                x1 = col * self.square_size
                y1 = row * self.square_size
                canvas.create_rectangle(
                    x1, y1, 
                    x1 + self.square_size, 
                    y1 + self.square_size, 
                    outline='red', 
                    width=3
                )
        else:
            try:
                if self.selected_board == board_num:
                    self.board.move_piece(
                        self.selected_piece, 
                        (row, col), 
                        board_num
                    )
                else:
                    self.board.move_piece(
                        self.selected_piece, 
                        (row, col), 
                        self.selected_board
                    )
                
                self.update_boards()
                
                self.selected_piece = None
                self.selected_board = None
            except ValueError as e:
                messagebox.showerror("Movimiento Inválido", str(e))
                self.selected_piece = None
                self.selected_board = None
                
            self.update_boards()

    def update_boards(self):
        """Actualizar visualización de ambos tableros"""
        for i, board_data in enumerate(self.board_frames):
            self.draw_board(board_data['canvas'], i+1)


    def make_ai_move(self):
        """Realizar movimiento de IA"""
        from ai import ChessAI
        
        ai = ChessAI(self.board, self.board.current_player)
        
        best_move = ai.choose_best_move()
        
        if best_move:
            try:
                start = (best_move[0], best_move[1])
                end = (best_move[2][0], best_move[2][1])
                board_num = best_move[3]  
                
                if board_num == 1:
                    self.board.move_piece(start, end, board_num)
                else:
                    self.board.move_piece(start, end, 2)
                
                self.update_boards()
            except Exception as e:
                messagebox.showerror("Error de IA", str(e))
        else:
            messagebox.showinfo("IA", "No hay movimientos posibles")

    def run(self):
        """Iniciar bucle principal de la interfaz"""
        self.window.mainloop()

def main():
    from board import Board
    
    board = Board()
    
    gui = ChessGUI(board)
    gui.run()

if __name__ == "__main__":
    main()
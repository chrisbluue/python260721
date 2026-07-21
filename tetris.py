import random
import tkinter as tk

WIDTH, HEIGHT = 10, 20
CELL_SIZE = 30
CANVAS_WIDTH = WIDTH * CELL_SIZE + 180
CANVAS_HEIGHT = HEIGHT * CELL_SIZE

SHAPES = {
    "I": [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    "O": [
        [1, 1],
        [1, 1],
    ],
    "T": [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0],
    ],
    "S": [
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0],
    ],
    "Z": [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 1],
    ],
    "J": [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    "L": [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ],
}

COLORS = {
    "I": "#00f0f0",
    "O": "#f0f000",
    "T": "#a000f0",
    "S": "#00f000",
    "Z": "#f00000",
    "J": "#0000f0",
    "L": "#f0a000",
}


def normalize_matrix(mat):
    rows = [list(r) for r in mat]

    while rows and not any(rows[0]):
        rows.pop(0)
    while rows and not any(rows[-1]):
        rows.pop()

    if not rows:
        return []

    cols = len(rows[0])
    while cols and not any(row[0] for row in rows):
        for row in rows:
            row.pop(0)
        cols -= 1

    while cols and not any(row[-1] for row in rows):
        for row in rows:
            row.pop()
        cols -= 1

    return rows


def rotate_matrix(mat):
    if not mat:
        return []
    rotated = [list(col) for col in zip(*mat[::-1])]
    return normalize_matrix(rotated)


class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Tetris")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#111111")
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.on_key)

        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.score = 0
        self.running = True
        self.active_piece = None

        self.start_game()

    def start_game(self):
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.score = 0
        self.running = True
        self.active_piece = self.new_piece()
        self.draw()
        self.root.after(500, self.tick)

    def new_piece(self):
        piece_name = random.choice(list(SHAPES.keys()))
        shape = [row[:] for row in SHAPES[piece_name]]
        piece = Piece(shape, COLORS[piece_name])
        piece.x = max(0, WIDTH // 2 - len(piece.shape[0]) // 2)
        piece.y = 0

        if self.collides(piece):
            self.running = False
        return piece

    def collides(self, piece, dx=0, dy=0, shape=None):
        shape_to_use = piece.shape if shape is None else shape
        for y, row in enumerate(shape_to_use):
            for x, cell in enumerate(row):
                if not cell:
                    continue
                nx = piece.x + x + dx
                ny = piece.y + y + dy
                if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
                    return True
                if ny >= 0 and self.board[ny][nx]:
                    return True
        return False

    def lock_piece(self):
        if self.active_piece is None:
            return

        for y, row in enumerate(self.active_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    ny = self.active_piece.y + y
                    if ny >= 0:
                        self.board[ny][self.active_piece.x + x] = 1

        self.clear_lines()
        self.active_piece = self.new_piece()
        if not self.running:
            self.draw()
            return

        self.draw()

    def clear_lines(self):
        new_board = [row for row in self.board if not all(row)]
        cleared = HEIGHT - len(new_board)
        self.score += cleared * 100
        while len(new_board) < HEIGHT:
            new_board.insert(0, [0] * WIDTH)
        self.board = new_board

    def move_piece(self, dx, dy):
        if self.active_piece is None or not self.running:
            return

        if not self.collides(self.active_piece, dx, dy):
            self.active_piece.x += dx
            self.active_piece.y += dy
            self.draw()
            return True

        if dy == 1:
            self.lock_piece()
        return False

    def rotate_piece(self):
        if self.active_piece is None or not self.running:
            return

        new_shape = rotate_matrix(self.active_piece.shape)

        for offset in (0, -1, 1, -2, 2):
            if not self.collides(self.active_piece, offset, 0, new_shape):
                self.active_piece.x += offset
                self.active_piece.shape = new_shape
                self.draw()
                return

    def hard_drop(self):
        if self.active_piece is None or not self.running:
            return

        while not self.collides(self.active_piece, 0, 1):
            self.active_piece.y += 1
        self.lock_piece()

    def tick(self):
        if not self.running:
            return

        if self.collides(self.active_piece, 0, 1):
            self.lock_piece()
        else:
            self.active_piece.y += 1
            self.draw()

        self.root.after(500, self.tick)

    def draw(self):
        self.canvas.delete("all")

        # draw board
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    self.draw_cell(x, y, "#666666")

        # draw current piece
        if self.active_piece is not None:
            for y, row in enumerate(self.active_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_cell(self.active_piece.x + x, self.active_piece.y + y, self.active_piece.color)

        # draw grid
        for y in range(HEIGHT + 1):
            self.canvas.create_line(0, y * CELL_SIZE, WIDTH * CELL_SIZE, y * CELL_SIZE, fill="#222222")
        for x in range(WIDTH + 1):
            self.canvas.create_line(x * CELL_SIZE, 0, x * CELL_SIZE, HEIGHT * CELL_SIZE, fill="#222222")

        # score text
        self.canvas.create_text(WIDTH * CELL_SIZE + 30, 30, text=f"Score: {self.score}", fill="white", anchor="nw", font=("Arial", 16, "bold"))

        # controls
        self.canvas.create_text(WIDTH * CELL_SIZE + 30, 80, text="Controls:", fill="white", anchor="nw", font=("Arial", 12, "bold"))
        self.canvas.create_text(WIDTH * CELL_SIZE + 30, 100, text="← → : Move", fill="white", anchor="nw")
        self.canvas.create_text(WIDTH * CELL_SIZE + 30, 120, text="↑ : Rotate", fill="white", anchor="nw")
        self.canvas.create_text(WIDTH * CELL_SIZE + 30, 140, text="↓ : Soft Drop", fill="white", anchor="nw")
        self.canvas.create_text(WIDTH * CELL_SIZE + 30, 160, text="Space : Hard Drop", fill="white", anchor="nw")
        self.canvas.create_text(WIDTH * CELL_SIZE + 30, 180, text="R : Restart", fill="white", anchor="nw")

        if not self.running:
            self.canvas.create_text(WIDTH * CELL_SIZE // 2, HEIGHT * CELL_SIZE // 2,
                                    text="GAME OVER", fill="red", font=("Arial", 28, "bold"))

    def draw_cell(self, x, y, color):
        if x < 0 or y < 0:
            return
        self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                     (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                     fill=color, outline="#222222")

    def on_key(self, event):
        if event.keysym == "r":
            self.start_game()
            return

        if not self.running:
            return

        if event.keysym == "Left":
            self.move_piece(-1, 0)
        elif event.keysym == "Right":
            self.move_piece(1, 0)
        elif event.keysym == "Down":
            self.move_piece(0, 1)
        elif event.keysym == "Up":
            self.rotate_piece()
        elif event.keysym == "space":
            self.hard_drop()


class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = 0
        self.y = 0


if __name__ == "__main__":
    root = tk.Tk()
    Tetris(root)
    root.mainloop()
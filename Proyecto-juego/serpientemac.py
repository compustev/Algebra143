
import tkinter as tk
import numpy as np
import random

# Configuración del juego
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 20

ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

GAME_SPEED = 120


class SnakeGame:

    def __init__(self, root):
        self.root = root
        self.root.title("El Gusanito - Juego con Matrices")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#111111"
        )
        self.canvas.pack()

        self.score_label = tk.Label(
            root,
            text="Puntuación: 0",
            font=("Arial", 14)
        )
        self.score_label.pack()

        # Matriz con las posiciones iniciales de la serpiente
        # Cada fila representa un segmento: [x, y]
        self.snake = np.array([
            [10, 10],
            [9, 10],
            [8, 10]
        ])

        # Matriz de movimientos
        self.transforms = {
            "Right": np.array([
                [1, 0, 0],
                [0, 1, 0],
                [1, 0, 1]
            ]),

            "Left": np.array([
                [1, 0, 0],
                [0, 1, 0],
                [-1, 0, 1]
            ]),

            "Up": np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, -1, 1]
            ]),

            "Down": np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, 1, 1]
            ])
        }

        self.direction = "Right"
        self.next_direction = "Right"

        self.food = self.create_food()
        self.score = 0
        self.game_over = False

        self.root.bind("<KeyPress>", self.change_direction)

        self.update_game()

    # Crear la matriz del tablero
    def create_board(self):
        board = np.zeros((ROWS, COLS), dtype=int)

        # Colocar la serpiente en la matriz
        for x, y in self.snake:
            board[y, x] = 1

        # Colocar el alimento
        fx, fy = self.food
        board[fy, fx] = 2

        return board

    # Generar alimento en una casilla vacía
    def create_food(self):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)

            if not any(
                np.array_equal([x, y], segment)
                for segment in self.snake
            ):
                return (x, y)

    # Cambiar la dirección
    def change_direction(self, event):
        key = event.keysym

        opposite = {
            "Right": "Left",
            "Left": "Right",
            "Up": "Down",
            "Down": "Up"
        }

        if key in self.transforms:
            if key != opposite[self.direction]:
                self.next_direction = key

    # Calcular la nueva posición mediante matrices
    def move_snake(self):
        self.direction = self.next_direction

        head = self.snake[0]

        # Convertir la posición en una coordenada homogénea
        head_matrix = np.array([
            head[0],
            head[1],
            1
        ])

        # Multiplicación matricial
        new_head_matrix = (
            head_matrix @ self.transforms[self.direction]
        )

        # Obtener las nuevas coordenadas
        new_head = new_head_matrix[:2]

        return new_head

    # Actualizar el juego
    def update_game(self):

        if self.game_over:
            return

        new_head = self.move_snake()

        x, y = new_head

        # Comprobar los límites del tablero
        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            self.finish_game()
            return

        # Comprobar colisión con el cuerpo
        if any(
            np.array_equal(new_head, segment)
            for segment in self.snake
        ):
            self.finish_game()
            return

        # Comprobar si comió el alimento
        if (x, y) == self.food:

            # Agregar la nueva cabeza sin eliminar la cola
            self.snake = np.vstack((
                new_head,
                self.snake
            ))

            self.score += 10

            self.score_label.config(
                text=f"Puntuación: {self.score}"
            )

            self.food = self.create_food()

        else:

            # Mover la serpiente conservando su longitud
            self.snake = np.vstack((
                new_head,
                self.snake[:-1]
            ))

        self.draw_game()

        self.root.after(
            GAME_SPEED,
            self.update_game
        )

    # Dibujar el tablero y sus elementos
    def draw_game(self):

        self.canvas.delete("all")

        # Obtener la matriz actual del tablero
        board = self.create_board()

        for y in range(ROWS):
            for x in range(COLS):

                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if board[y, x] == 1:
                    color = "lime"

                elif board[y, x] == 2:
                    color = "red"

                else:
                    color = "#111111"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#292929"
                )

    # Terminar el juego
    def finish_game(self):

        self.game_over = True

        self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            text="¡JUEGO TERMINADO!",
            fill="red",
            font=("Arial", 20, "bold")
        )


# Ejecutar el programa
if __name__ == "__main__":

    root = tk.Tk()

    game = SnakeGame(root)

    root.mainloop()

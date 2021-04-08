import tkinter as tk
from random import randint

from PIL import Image, ImageTk

MOVE_INCREMENT = 20
moves_per_second = 10
GAME_SPEED = 1000 // moves_per_second


class Snake(tk.Canvas):
    def __init__(self, root):
        super().__init__(width=600,
                         height=620,
                         background='black',
                         highlightthickness=0)  # Border 0
        self.root = root
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self._set_new_food_position()
        self.score = 0
        self.level = 0
        self.direction = 'Right'
        self.bind_all('<Key>', self._on_key_press)

        # -- LOAD ASSETS --
        try:
            self.snake_body_image = Image.open('./assets/snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.snake_food_image = Image.open('./assets/food.png')
            self.snake_food = ImageTk.PhotoImage(self.snake_food_image)
        except IOError as error:
            print(error)
            self.root.destroy()
        # --

        self.create_objects()
        self.after(GAME_SPEED, self.perform_actions)

    def create_objects(self):
        self.create_text(45,
                         12,
                         text=f"Score: {self.score}",
                         tag='score',
                         fill='#fff',
                         font=('TkDefaultFont', 14))

        print(self.winfo_width())

        self.create_text(555,
                         12,
                         text=f"Level: {self.level}",
                         tag='level',
                         fill='#fff',
                         font=('TkDefaultFont', 14))

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position,
                              y_position,
                              image=self.snake_body,
                              tag='snake')

        self.create_image(*self.food_position,
                          image=self.snake_food,
                          tag='food')

        self.create_rectangle(7, 27, 593, 613, outline='#525d69')

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == 'Left':
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Right':
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Down':
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == 'Up':
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return

        self._check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
                head_x_position in (0, 600)
                or head_y_position in (20, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def _check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0 :
                global moves_per_second
                moves_per_second += 1
                self.level += 1
                level = self.find_withtag('level')
                self.itemconfigure(level, text=f"Level: {self.level}", tag='level')

            self.create_image(
                *self.snake_positions[-1],
                image=self.snake_body,
                tag='snake',
            )

            self.food_position = self._set_new_food_position()
            print(self.food_position)
            self.coords(self.find_withtag('food'), self.food_position)

            score = self.find_withtag('score')
            self.itemconfigure(score, text=f"Score: {self.score}", tag='score')

    def _set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game Over! You scored {self.score}!",
            fill='#fff',
            font=('TkDefaultFont', 24)
        )

    def _on_key_press(self, event):
        new_direction = event.keysym
        all_directions = ('Up', 'Down', 'Left', 'Right')
        opposites = ({*all_directions[:2]}, {*all_directions[-2:]})

        if (new_direction in all_directions
                and {new_direction, self.direction} not in opposites):
            self.direction = event.keysym

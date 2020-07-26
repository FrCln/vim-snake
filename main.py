from random import randint
from tkinter import Tk, Canvas, Label

from snake import Snake, Segment


WIDTH = 800
HEIGHT = 600
SEG = 20
BG_SIDE = '#777777'
BG_FIELD = '#005500'


class Game:

    def __init__(self):
        self.in_game = True
        self.add = False
        self.job = None
        self.score = 0
        self.keys = {
            'j': 'Down',
            'k': 'Up',
            'h': 'Left',
            'l': 'Right',
        }

        self.root = Tk()
        self.root.title('Python Snake')
        self.canvas = Canvas(self.root, width=WIDTH + 250, height=HEIGHT, bg=BG_SIDE)
        self.canvas.grid()
        self.score_label = Label(self.canvas, width=8, height=2, font='Impact 36', bg=BG_SIDE)
        self.score_label.place(x=WIDTH + 10, y=100)
        self.score_label.configure(text='Очки:\n0')
        self.hint_label = Label(self.canvas, width=11, height=6, font='Impact 36', bg=BG_SIDE)
        self.hint_label.place(x=WIDTH + 10, y=200)
        self.hint_label.configure(
            text='Управление:\n'
            'H: Влево\n'
            'J: Вниз\n'
            'K: Вверх\n'
            'L: Вправо\n'
            'Esc: Выход\n'
        )
        self.canvas.focus_set()
        self.draw_field()
        self.snake = Snake(self.canvas, SEG)
        self.apple = None
        self.create_apple()

    def run(self):
        self.canvas.bind("<KeyPress>", self.key_event_handler)
        self.main_loop()
        self.root.mainloop()

    def key_event_handler(self, event):
        if event.keysym in self.keys:
            self.snake.change_direction(self.keys[event.keysym])
        if event.keysym == 'Escape':
            self.root.after_cancel(self.job)
            exit(0)

    def snake_intersection(self):
        head = self.canvas.coords(self.snake.segments[-1].instance)
        return any(
            self.canvas.coords(segment.instance) == head
            for segment in self.snake.segments[:-1]
        )

    def main_loop(self):
        if self.in_game:
            self.snake.move(self.add)
            if self.add:
                self.delete_apple()
                self.create_apple()
                self.update_score()
                self.add = False
            x1, y1, x2, y2 = self.canvas.coords(self.snake.segments[-1].instance)
            if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT or self.snake_intersection():
                self.in_game = False
            if self.apple in self.canvas.find_overlapping(x1 + 1, y1 + 1, x2 - 1, y2 - 1):
                self.add = True
        self.job = self.root.after(100, self.main_loop)

    def delete_apple(self):
        self.canvas.delete(self.apple)
        self.apple = None

    def create_apple(self):
        while not self.apple or any(
            self.apple in self.canvas.find_overlapping(*self.canvas.coords(x.instance))
            for x in self.snake.segments):
            if self.apple:
                self.canvas.delete(self.apple)
            x = SEG * randint(1, WIDTH // SEG - 1)
            y = SEG * randint(1, HEIGHT // SEG - 1)
            self.apple = self.canvas.create_oval(x, y, x + SEG, y + SEG, fill='red')

    def draw_field(self):
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG_FIELD)

    def update_score(self):
        self.score += 1
        self.score_label.configure(text=f'Очки:\n{self.score}')


if __name__ == '__main__':
    game = Game()
    game.run()

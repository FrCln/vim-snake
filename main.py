from tkinter import *
from random import randint

WIDTH = 800
HEIGHT = 600
SEG = 20
BG_SIDE = '#777777'
BG_FIELD = '#005500'
IN_GAME = True
ADD = False

score = 0


class Segment():
    def __init__(self, canvas, x, y):
        self.instance = \
            canvas.create_rectangle(x, y, x+SEG, y+SEG, fill='white')
        self.canvas = canvas


class Snake():
    def __init__(self, canvas, segments):
        self.segments = segments
        self.canvas = canvas

        self.mapping = {
            'Down': (0, 1),
            'Up': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }

        self.vector = self.mapping['Right']

    def move(self, add_segment=False):
        if not add_segment:
            self.canvas.delete(self.segments[0].instance)
            self.segments.pop(0)
        x, y, *other = self.canvas.coords(self.segments[-1].instance)
        self.segments.append(Segment(canvas,
                                     x + self.vector[0]*SEG,
                                     y + self.vector[1]*SEG))

    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]
        if event.keysym == 'Escape':
            exit()

    def reset_snake(self):
        for seg in self.segments:
            self.canvas.delete(seg.instance)
        self.segments.clear()


def create_snake(canvas):
    segments = [Segment(canvas, SEG, SEG),
                Segment(canvas, SEG*2, SEG),
                Segment(canvas, SEG*3, SEG)]
    return Snake(canvas, segments)


def snake_intersection(snake):
    head = canvas.coords(snake.segments[-1].instance)
    return any(canvas.coords(segment.instance) == head for segment in snake.segments[:-1])


def in_game():
    global IN_GAME
    global ADD
    if IN_GAME:
        snake.move(ADD)
        if ADD:
            canvas.delete(apple)
            create_apple(canvas)
            update_score()
            ADD = False
        x1, y1, x2, y2 = canvas.coords(snake.segments[-1].instance)
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT or snake_intersection(snake):
            IN_GAME = False
        if apple in canvas.find_overlapping(x1 + 1, y1 + 1, x2 - 1, y2 - 1):
            ADD = True
    root.after(100, in_game)


def create_apple(canvas):
    global apple
    apple = None
    while not apple or \
    any(apple in canvas.find_overlapping(*canvas.coords(x.instance)) for x in snake.segments):
        if apple:
            canvas.delete(apple)
        x = SEG * randint(1, WIDTH // SEG - 1)
        y = SEG * randint(1, HEIGHT // SEG - 1)
        apple = canvas.create_oval(x, y, x + SEG, y + SEG, fill='red')


def draw_glass():
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG_FIELD)


def update_score():
    global score
    score += 1
    score_label.configure(text=f'Очки:\n{score}')


root = Tk()

root.title('Python Snake')
canvas = Canvas(root, width=WIDTH + 200, height=HEIGHT, bg=BG_SIDE)
canvas.grid()
score_label = Label(canvas, width=8, height=2, font='Impact 36', bg=BG_SIDE)
score_label.place(x=WIDTH + 10, y=100)
score_label.configure(text=f'Очки:\n0')
canvas.focus_set()
draw_glass()
snake = create_snake(canvas)
create_apple(canvas)

canvas.bind("<KeyPress>", snake.change_direction)
in_game()

root.mainloop()

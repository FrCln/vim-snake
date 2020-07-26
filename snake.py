from tkinter import Canvas


class Segment():
    def __init__(self, canvas: Canvas, x, y, seg_size):
        self.instance = \
            canvas.create_rectangle(x, y, x+seg_size, y+seg_size, fill='white')
        self.canvas = canvas


class Snake():
    def __init__(self, canvas: Canvas, seg_size):
        self.canvas = canvas
        self.seg_size = seg_size
        self.segments = [
            Segment(canvas, seg_size, seg_size, seg_size),
            Segment(canvas, seg_size*2, seg_size, seg_size),
            Segment(canvas, seg_size*3, seg_size, seg_size),
        ]
        self.mapping = {
            'Down': (0, 1),
            'Up': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0),
        }

        self.vector = self.mapping['Right']

    def move(self, add_segment=False):
        if not add_segment:
            self.canvas.delete(self.segments[0].instance)
            self.segments.pop(0)
        x, y, *other = self.canvas.coords(self.segments[-1].instance)
        self.segments.append(Segment(self.canvas,
                                     x + self.vector[0] * self.seg_size,
                                     y + self.vector[1] * self.seg_size,
                                     self.seg_size))

    def change_direction(self, direction):
        self.vector = self.mapping[direction]

    def reset_snake(self):
        for seg in self.segments:
            self.canvas.delete(seg.instance)
        self.segments.clear()

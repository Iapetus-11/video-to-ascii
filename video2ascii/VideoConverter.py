import ffmpeg
import numpy as np
import typing
import math

from Video import *
from Viewer import *

gradients = [
    '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,^.\'\"` ',
    '@%#*+=-:. ',
    '█▓▒░ '
]

class VideoConverter:
    def __init__(self, *, w: int, h: int, file_name: str, scaled_w: int = 100, stretch: float = 1, gradient: typing.Union[int, str] = 0):
        self.w = w
        self.h = h

        self.aspect_ratio = self.w/self.h
        self.stretch = stretch

        self.sw = scaled_w*self.stretch
        self.sh = int(math.ceil(self.aspect_ratio*self.h))

        self.file_name = file_name
        self.video = Video(w=self.w, h=self.h, file_name=self.file_name)
        self.video_input = self.video.video_input.video
        self.fps = self.video.fps

        self.process = None

        self.frames = None
        self.viewer = None

        if isinstance(gradient, int):
            if 0 <= gradient < len(gradients):
                self.grad = gradients[gradient]
            else:
                self.grad = gradients[0]
        else:
            self.grad = gradient

    def get_ascii_pixel(self, p):  # takes [r, g, b]
        avg = (int(p[0]) + int(p[1]) + int(p[2])) / 3
        return self.grad[int((avg*(len(self.grad)-1))/255)]

    def convert(self):
        self.video_input = self.video_input.filter('scale', self.sw, self.sh)

        self.process = self.video_input.output('pipe:', format='rawvideo', pix_fmt='rgb24').run_async(pipe_stdout=True)

        self.frames = []

        while True:
            bytes_in = self.process.stdout.read(self.sw * self.sh * 3)

            if not bytes_in:
                break

            # frame is essentially a list of rgb [[r, g, b], [r, g, b], [r, g, b],...]
            frame = np.frombuffer(bytes_in, np.uint8).reshape([self.sh, self.sw, 3]).copy()
            # frame[0][0] is [r, g, b], frame is 2d array / matrix

            frame_new = []

            for i, row in enumerate(frame):
                frame_new.append([])
                for col in row:
                    frame_new[i].append(self.get_ascii_pixel(col))

            self.frames.append(frame_new)  # append asciified frame

        self.viewer = Viewer(self.__dict__)
        return self.viewer

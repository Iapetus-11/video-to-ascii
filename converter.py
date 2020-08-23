import classyjson  # classy-json
import ffmpeg  # ffmpeg-python
import numpy  # numpy
import time
import math
import os

with open('config.json', 'r') as c:
    config = classyjson.load(c)

config.gradients[0] = ''.join(reversed([c for c in config.gradients[0]]))
config.gradients[1] = ''.join(reversed([c for c in config.gradients[1]]))

# for test1
"""
h = 540
w = 960

aspect_ratio = w/h

sh = 175
sw = math.ceil(aspect_ratio*sh)
"""

h = 320
w = 320

aspect_ratio = w/h

sh = 150
sw = math.floor(math.ceil(aspect_ratio*sh)*1.5)

vid_inp = ffmpeg.input('test2.mp4')
vid_inp = vid_inp.video.filter('scale', sw, sh)
process = vid_inp.output('pipe:', format='rawvideo', pix_fmt='rgb24').run_async(pipe_stdout=True)

frames = []  # will be list of asciified frames

def get_ascii_pixel(p):  # takes [r, g, b]
    avg = (int(p[0]) + int(p[1]) + int(p[2])) / 3
    grad = config.gradients[1]
    return grad[int((avg*(len(grad)-1))/255)]

while True:
    bytes_in = process.stdout.read(sh * sw * 3)

    if not bytes_in:
        break

    # frame is essentially a list of rgb [[r, g, b], [r, g, b], [r, g, b],...]
    #frames.append(numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]))
    frame = numpy.frombuffer(bytes_in, numpy.uint8).reshape([sh, sw, 3]).copy()
    # frame[0][0] is [r, g, b], frame is 2d array / matrix duh

    frame_new = []

    for i, row in enumerate(frame):
        frame_new.append([])
        for col in row:
            frame_new[i].append(get_ascii_pixel(col))

    frames.append(frame_new)  # append asciified frame

# test
for frame in frames:
    #print('\n'*50)
    os.system('cls')
    body = ''
    for row in frame:
        body += '\n' + ''.join(row)
    print(body)
    time.sleep(.05)

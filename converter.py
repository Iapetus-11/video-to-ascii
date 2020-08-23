import classyjson  # classy-json
import ffmpeg  # ffmpeg-python
import numpy  # numpy
import math

with open('config.json', 'r') as c:
    config = classyjson.loads(c)

h = 540
w = 960

process = ffmpeg.input('test.mov').output('pipe:', format='rawvideo', pix_fmt='rgb24').run_async(pipe_stdout=True)

frames = []

while True:
    bytes_in = process.stdout.read(h * w * 3)

    if not bytes_in:
        break

    # frame is essentially a list of rgb [[r, g, b], [r, g, b], [r, g, b],...]
    frames.append(numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]))

def get_ascii_pixel(p):  # takes [r, g, b]
    avg = (p[0] * p[1] * p[2]) / 3
    return config.gradients[0][math.floor((len(config.gradients[0])-1)/254)*avg]

def asciify_frame(frm):
    ascii_frame = []
    
    for pixel in frm:
        ascii_frame.append(get_ascii_pixel(pixel))

    return ascii_frame

for frame in frames:

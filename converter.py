import classyjson  # classy-json
import ffmpeg  # ffmpeg-python
import numpy  # numpy
import math

with open('config.json', 'r') as c:
    config = classyjson.load(c)

h = 540
w = 960

process = ffmpeg.input('test.mov').output('pipe:', format='rawvideo', pix_fmt='rgb24').run_async(pipe_stdout=True)

frames = []  # will be list of asciified frames

def get_ascii_pixel(p):  # takes [r, g, b]
    avg = (p[0] * p[1] * p[2]) / 3
    return config.gradients[0][math.floor((((len(config.gradients[0])-1)/254)*avg))]

while True:
    bytes_in = process.stdout.read(h * w * 3)

    if not bytes_in:
        break

    # frame is essentially a list of rgb [[r, g, b], [r, g, b], [r, g, b],...]
    #frames.append(numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]))
    frame = numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]).copy()
    # frame[0][0] is [r, g, b], frame is 2d array / matrix duh

    frame_new = []

    for i in range(len(frame)):  # rows
        print(f'i: {i}/{len(frame)}')
        for j in range(len(frame[i])):  # columns
            print(f'j: {j}/{len(frame[i])}')
            frame_new[i].append(get_ascii_pixel(frame[i+1][j+1]))

    for i, row in enumerate(frame):
        for col in row:
            frame_new[i].append(get_ascii_pixel(col))

    frames.append(frame_new)  # append asciified frame

# test
for frame in frames:
    print(frame)
    exit(0)

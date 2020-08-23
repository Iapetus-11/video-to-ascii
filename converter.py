import classyjson  # classy-json
import ffmpeg  # ffmpeg-python
import numpy  # numpy
import time

with open('config.json', 'r') as c:
    config = classyjson.load(c)

print(f'Config: {config}')

h = 540
w = 960

process = ffmpeg.input('test.mov').output('pipe:', format='rawvideo', pix_fmt='rgb24').run_async(pipe_stdout=True)

frames = []  # will be list of asciified frames

def get_ascii_pixel(p):  # takes [r, g, b]
    avg = (int(p[0]) + int(p[1]) + int(p[2])) / 3
    grad = config.gradients[0]
    return grad[int((avg*(len(grad)-1))/255)]

while True:
    bytes_in = process.stdout.read(h * w * 3)

    if not bytes_in:
        break

    # frame is essentially a list of rgb [[r, g, b], [r, g, b], [r, g, b],...]
    #frames.append(numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]))
    frame = numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]).copy()
    # frame[0][0] is [r, g, b], frame is 2d array / matrix duh

    frame_new = []

    for i, row in enumerate(frame):
        frame_new.append([])
        for col in row:
            frame_new[i].append(get_ascii_pixel(col))

    frames.append(frame_new)  # append asciified frame

# test
for frame in frames:
    print('\n'*50)
    print('\n'.join(frame))
    time.sleep(1)

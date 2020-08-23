import ffmpeg # ffmpeg-python
import numpy

h = 540
w = 960

process = ffmpeg.input('test.mov').output('pipe:', format='rawvideo', pix_fmt='rgb24').run_async(pipe_stdout=True)

frames = []

while True:
    bytes_in = process.stdout.read(h * w * 3)

    if not bytes_in:
        break

    frames.append(numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]))

print(frames[0])
print(type(frames[0]))
print(len(frames))

with open('dump', 'w+') as f:
    f.write(frames.dumps())

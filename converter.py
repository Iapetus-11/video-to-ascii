import ffmpeg # ffmpeg-python
import numpy

inp = ffmpeg.input('test.mov')
process = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', input=inp).run_async(pipe_stdout=True)

frames = []

while True:
    bytes_in = process.stdout.read(h, w, 3)

    if not bytes_in:
        break

    frames.append(numpy.frombuffer(bytes_in, numpy.uint8).reshape([h, w, 3]))

print(len(frames))

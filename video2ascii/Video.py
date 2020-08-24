import ffmpeg
import os
import subprocess


class FileNotFound(Exception):
    def __init__(self, file: str, msg: str = 'File \'{0}\' not found!'):
        self.msg = msg.format(file)

    def __str__(self):
        return self.msg


def get_fps(file_name):
    out = subprocess.check_output(["ffprobe", file_name, "-v", "0", "-select_streams", "v", "-print_format", "flat", "-show_entries", "stream=r_frame_rate"])
    rate = out.split('=')[1].strip()[1:-1].split('/')

    if len(rate) == 1:
        return float(rate[0])

    if len(rate) == 2:
        return float(rate[0])/float(rate[1])

    return 30


class Video:
    def __init__(self, *, w: int, h: int, file_name: str):
        self.w = w
        self.h = h

        self.file_name = file_name

        if not os.path.isfile(self.file_name):
            raise FileNotFound(self.file_name)

        if not os.path.isfile('ffmpeg.exe'):
            print(f'\n\nERROR: You must download ffmpeg.exe and install it in this directory: \'{os.getcwd()}\'\n')
            exit(0)

        self.fps = get_fps(self.file_name)

        self.video_input = ffmpeg.input(file_name)

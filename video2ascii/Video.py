import ffmpeg
import os


class FileNotFound(Exception):
    def __init__(self, file: str, msg: str = 'File \'{0}\' not found!'):
        self.msg = msg.format(file)

    def __str__(self):
        return self.msg


class Video:
    def __init__(self, *, w: int, h: int, file_name: str):
        self.w = w
        self.h = h

        self.file_name = file_name

        if not os.path.isfile(self.file_name):
            raise FileNotFound(self.file_name)

        if not os.path.isfile('ffmpeg.exe'):
            print(f'You must download ffmpeg.exe and install it in this directory: \'{os.getcwd()}\'')
            exit(0)

        self.video_input = ffmpeg.input(file_name)

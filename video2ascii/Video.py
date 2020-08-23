import ffmpeg


class Video:
    def __init__(self, *, w: int, h: int, file_name: str):
        self.w = w
        self.h = h

        self.file_name = file_name

        self.video_input = ffmpeg.input(file_name)

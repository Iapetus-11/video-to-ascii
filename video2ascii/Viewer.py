from time import sleep
import os

class Viewer:
    def __init__(self, meta):
        for attr in meta.keys():
            self.__dict__[attr] = meta[attr]

    def view_frame(self, f_index: int):
        frame = self.frames[f_index]
        body = ''

        for row in frame:
            body += '\n' + ''.join(row)

        print(body)

    def _view_frame(self, frame):
        os.system('cls')

        body = ''

        for row in frame:
            body += '\n' + ''.join(row)

        print(body)

    def view(self):
        for frame in self.frames:
            self._view_frame(frame)
            sleep(.05)
            #sleep(1/self.fps)

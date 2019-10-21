import cv2
import os

class process_unit:
    def __init__(self):
        self.video = None
        self.video_path = None
        if os.path.exists('./frames'):
            self.frame_path = './frames/'
        else:
            self.frame_path = None
        self.frames = []

    def read_video(self, path):
        self.video = cv2.VideoCapture(path)
        self.video_path = path

    def make_frames(self):
        if self.video is not None:
            success, image = self.video.read()
            count = 0
            self.frame_path = "./frames/"
            while success:
                success, image = self.video.read()
                cv2.imwrite("./frames/%d.jpg" % count, image)
                count += 1
                print("count: %d" % count)
        else:
            print('read video first!')

    def read_frames(self):
        if self.frame_path is not None:
            for (dirpath, dirnames, filenames) in os.walk(self.frame_path):
                filenames.sort(key=lambda x: int(os.path.splitext(x)[0]))
                for name in filenames:
                    full_path = self.frame_path+name
                    self.frames.append(full_path)
                break
        else:
            return

if __name__ == '__main__':
    test = process_unit()
    test.read_video('./5.mp4')
    test.make_frames()
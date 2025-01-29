import tkinter
import cv2
import numpy as np
from PIL import Image, ImageTk


class VideoController:
    """
    Controls a canvas for use with video playback and display
    """

    def __init__(self, root, canvas, output):
        self.root = root
        self.fps = None
        self.frameTime = None
        self.path = None
        self.data = None
        self.output = output
        self.canvas = canvas
        self.pause = False

        canvas.update()
        self.size = (canvas.winfo_width(), canvas.winfo_height())
        self.canvas.config(width=self.size[0], height=self.size[1])

    def loadVideo(self, path):
        self.path = path
        self.data = cv2.VideoCapture(path)
        if not self.data.isOpened():
            self.output("Failed to load video data!", error=True)

        self.fps = self.data.get(cv2.CAP_PROP_FPS)
        self.frameTime = 1 / self.fps
        self.updateFrame(True)

    def updateFrame(self, single=False):
        if self.pause:
            return

        res, frame = self.data.read()
        if res:
            self.root.update_idletasks()
            self.size = (self.canvas.winfo_width(), self.canvas.winfo_height())

            resizedFrame = cv2.resize(frame, self.size, interpolation=cv2.INTER_AREA)
            frameRgb = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2RGB)
            frameImage = Image.fromarray(frameRgb)
            frameTk = ImageTk.PhotoImage(frameImage)

            self.canvas.create_image(0, 0, anchor=tkinter.NW, image=frameTk)
            self.canvas.image = frameTk

            if not single:
                self.root.after(int(self.frameTime * 1000), self.updateFrame)
        else:
            # End of video
            self.data.release()

    def playVideo(self):
        self.pause = False
        self.updateFrame()

    def pauseVideo(self):
        self.pause = True

    def skipEnd(self):
        pass

    def reset(self):
        self.data.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.updateFrame(True)


def convert_video_to_x_fps(vidcap, fps_out, output, print_flag=True):
    """
    Converts video to given framerate

    :param vidcap: -- Video to change | Must be in cv2.VideoCapture format
    :param fps_out: -- Framerate to set video to
    :param output: -- Console output location
    :param print_flag: -- Print debug data (default True)
    :return:
    """

    fps_in = vidcap.get(cv2.CAP_PROP_FPS)
    if print_flag:
        output("fps_in: ", fps_in)
        output("fps_out: ", fps_out)

    index_in = -1
    index_out = -1

    frames = []
    while True:
        success = vidcap.grab()
        if not success: break
        index_in += 1

        out_due = int(index_in / fps_in * fps_out)
        if out_due > index_out:
            success, frame = vidcap.retrieve()
            if not success: break
            index_out += 1

            frames.append(frame)

    return frames


def convert_video_to_frames(cv2_capture, frame_rate, crop_video_length, return_consistent_length=False, print_flag=True):
    """
    If the video is shorter than frame_rate frames, it will be padded with images of zeros
    If the video is longer than frame_rate frames, it will be split into multiple sets of video_length.
    """

    frames = convert_video_to_x_fps(cv2_capture, frame_rate, print_flag=print_flag)

    frame_rate_crop_video_length = round(frame_rate * crop_video_length)  # Target length of each clip expressed in frames

    frames_clips = []
    for i in range(len(frames), -1, -frame_rate_crop_video_length):
        if i - frame_rate_crop_video_length - 1 < 0:
            frames_clips.append(frames[0:i])
        else:
            frames_clips.append(frames[i - frame_rate_crop_video_length:i])
    frames_clips.reverse()

    if return_consistent_length:
      for i in range(len(frames_clips[0]), frame_rate_crop_video_length):
            frames_clips[0].append(np.zeros(frames_clips[0][0].shape, dtype=type(frames_clips[0][0][0][0])))

    if print_flag:
        print("\n__convert_video_to_frames__")
        print("original clips len(frames): ", len(frames))
        print("len(frames_clips): ", len(frames_clips))
        len_of_clips = [len(frames_clips[i]) for i in range(len(frames_clips))]
        print("Small clip has length: ", min(len_of_clips), " at index: ", len_of_clips.index(min(len_of_clips)))
        print("Big clip has length: ", max(len_of_clips), " at index: ", len_of_clips.index(max(len_of_clips)))

    return frames_clips

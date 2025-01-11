import time

import json
import cv2
import matplotlib.pyplot as plt
import torch
from mmpose.apis import MMPoseInferencer

from utils import video

# GREAT NEWS! YOU HAVE TO USE NUMPY V 1.26.4 AND TORCH 2.3.1 WHY? IDK FUCK YOU THATS WHY!
# also this: https://mmcv.readthedocs.io/en/latest/get_started/installation.html

# https://github.com/rishiswethan/TestingPose/blob/main/experiments/test/test_mmpose.py
# looked here
# yeah turns out basically all this code has been written before
# still suffered tho

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)


def visualize_keypoints(img_path, keypoints, pairs):
    # Load the image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Normalize keypoints to the size of the image
    height, width, _ = img.shape
    keypoints = [(int(x * width), int(y * height)) for x, y, _ in keypoints]

    # Draw keypoints and lines on the image
    for point in keypoints:
        cv2.circle(img, point, 3, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    for pair in pairs:
        cv2.line(img, keypoints[pair[0]], keypoints[pair[1]], (0, 255, 0), 2)

    return img


class InferMedia:
    def __init__(self, output, device=device):
        self.output = output
        # output(f"Using [{device}] device")
        # self.inferencer = MMPoseInferencer('human')
        # TODO: this should be changed to pass in a custom trained model parameter eventually.
        self.twoDimInferencer = MMPoseInferencer('human')
        self.threeDimInferencer = MMPoseInferencer(pose3d='human3d', device=device)

    # def infer_image(self, img_path, return_vis=False, save_vis=False):
    #     output_dir = "vis" if save_vis else None
    #
    #     result_generator = self.twoDimInferencer(img_path, show=False, out_dir=output_dir, return_vis=return_vis)
    #     result = next(result_generator)
    #
    #     preds = result['predictions'][0]
    #
    #     if return_vis:
    #         result_vis = result['visualization'][0]
    #
    #         return result_vis, preds
    #     else:
    #         return preds

    def infer_video_two_dim(self, video_path, return_vis=True, adjusted_fps = 0):

        fps = adjusted_fps if adjusted_fps > 0 else cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)

        frames = video.convert_video_to_x_fps(cv2.VideoCapture(video_path), fps_out=fps, print_flag=True)

        total_frames = len(frames)
        # self.output("len(frames): ", total_frames)

        result_generator = self.twoDimInferencer(frames, show=False, out_dir=None, return_vis=return_vis)

        results = next(result_generator)

        visualisations = []
        preds = []

        start_time = time.time()

        inc = 0
        for result in result_generator:
            plt.clf()  # Clear the plot

            preds.append(result['predictions'][0])

            if return_vis:
                vis = result['visualization'][0]
                visualisations.append(vis)

            finished_perc = int(len(preds)/total_frames*20)

            if inc == 5:
                inc = 0
                # self.output(f"Loading Visuals... {round((len(preds)/total_frames) * 100, 1)}%")

            inc += 1

        # self.output(f"Loading Visuals... 100%")

        plt.clf()  # Clear the plot
        time_taken = time.time() - start_time

        # self.output(f"Frame Count: {len(frames)}")
        # self.output(f"Total Time: {round(time_taken, 3)}s")
        # self.output(f"Time Per Frame: {round(time_taken / len(frames), 3)}s")

        yield visualisations
        yield preds


    def infer_video_three_dim(self, video_path, return_vis=True, adjusted_fps = 0):

        fps = adjusted_fps if adjusted_fps > 0 else cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)

        frames = video.convert_video_to_x_fps(cv2.VideoCapture(video_path), fps_out=fps, print_flag=True)

        total_frames = len(frames)
        # self.output("len(frames): ", total_frames)

        result_generator = self.threeDimInferencer(frames, show=False, out_dir=None, return_vis=return_vis)

        results = next(result_generator)

        visualisations = []
        preds = []

        start_time = time.time()

        inc = 0
        for result in result_generator:
            plt.clf()  # Clear the plot

            preds.append(result['predictions'][0])

            if return_vis:
                vis = result['visualization'][0]
                visualisations.append(vis)

            finished_perc = int(len(preds)/total_frames*20)

            if inc == 5:
                inc = 0
                # self.output(f"Loading Visuals... {round((len(preds)/total_frames) * 100, 1)}%")

            inc += 1

        # self.output(f"Loading Visuals... 100%")

        plt.clf()  # Clear the plot
        time_taken = time.time() - start_time

        # self.output(f"Frame Count: {len(frames)}")
        # self.output(f"Total Time: {round(time_taken, 3)}s")
        # self.output(f"Time Per Frame: {round(time_taken / len(frames), 3)}s")

        yield visualisations
        yield preds


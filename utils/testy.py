import sys
from sys import stdout

from utils.model import InferMedia
from utils.pipers import visualize_movie

inferMedia = InferMedia(stdout)

# INPUT 0 FPS IF YOU WANT TO USE ORIGINAL VIDEO FPS
# save_path is the way to get to save location
# file name is what to name the file
# DO NOT ADD .MP4 TO THE FILENAME (probably breaks it idk i didnt test it) :D
path = visualize_movie(video_path='test_data/3197604-hd_1080_1920_25fps.mp4', save_path='movie/boom.mp4', adjusted_fps=2, inferrer=inferMedia, output=stdout, threeDim=False)
# ^Output                         Input Path^                                         Save At^                     FPS^         Model^           Output^         3d^
print(path[0]) # <-- Location of Video
poses = path[1] # <-- pose points

#format
print("-=-=-=-=-=-=-=-=-=-=-=-")
for pose in poses:
    print(pose[0]['keypoints']) # Accessing data?
    print(pose[0]['keypoint_scores'])
    print("-=-=-=-=-=-=-=-=-=-=-=-")

# 2D points should be in screen space (i think?)
# Keypoints are connected by a predefined skeleton structure

# This base model uses the COCO Structure
# Connections:
# (0, 1), (0, 2), (1, 3), (2, 4)  Face
# (5, 6), (5, 7), (7, 9), (6, 8), (8, 10)  Arms
# (11, 12), (5, 11), (6, 12)  Torso
# (11, 13), (13, 15), (12, 14), (14, 16)  Legs
# 0	Nose
# 1	Left Eye
# 2	Right Eye
# 3	Left Ear
# 4	Right Ear
# 5	Left Shoulder
# 6	Right Shoulder
# 7	Left Elbow
# 8	Right Elbow
# 9	Left Wrist
# 10 Right Wrist
# 11 Left Hip
# 12 Right Hip
# 13 Left Knee
# 14 Right Knee
# 15 Left Ankle
# 16 Right Ankle

## bbox is the bounding box of the person


# path = visualize_movie(video_path='test_data/3197604-hd_1080_1920_25fps.mp4', save_path='movie/boom.mp4', adjusted_fps=2, inferrer=inferMedia, output=stdout, threeDim=True)
#
# print(next(path))
# poses = next(path)
# for pose in poses:
#     print(pose)

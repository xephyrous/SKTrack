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
print(next(path)) # <-- Location of Video
poses = next(path) # <-- pose points

#format
print("-=-=-=-=-=-=-=-=-=-=-=-")
for pose in poses:
    print(pose[0]['keypoints']) # Accessing data?
    print(pose[0]['keypoint_scores'])
    print("-=-=-=-=-=-=-=-=-=-=-=-")


# path = visualize_movie(video_path='test_data/3197604-hd_1080_1920_25fps.mp4', save_path='movie/boom.mp4', adjusted_fps=2, inferrer=inferMedia, output=stdout, threeDim=True)
#
# print(next(path))
# poses = next(path)
# for pose in poses:
#     print(pose)

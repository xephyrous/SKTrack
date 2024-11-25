from utils.model import Infer3D
from utils.pipers import visualize_movie

infer3d = Infer3D()

# INPUT 0 FPS IF YOU WANT TO USE ORIGINAL VIDEO FPS
# save_path is the way to get to save location
# file name is what to name the file
# DO NOT ADD .MP4 TO THE FILENAME (probably breaks it idk i didnt test it) :D
path = visualize_movie(video_path='test_data/3197604-hd_1080_1920_25fps.mp4', save_path='movie', file_name="BOOM", adjusted_fps=2, inferer=infer3d)
# ^Output                         Input Path^                                     Save At^            File Name^              FPS^         Model^
print(path) # <-- Location of Video
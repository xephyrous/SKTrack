import os.path

import cv2

def visualize_movie(video_path, save_path, file_name, adjusted_fps, inferer):

    fps = adjusted_fps if adjusted_fps > 0 else cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)

    print('Frames per second: %.2f' % fps)

    results = inferer.infer_video(video_path, return_vis=True, adjusted_fps=fps)

    if len(results) == 0:
        print('No results')
        return

    height, width, channels = results[0].shape

    if not (os.path.exists(save_path)):
        os.makedirs(save_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(save_path+"/"+file_name+".mp4", fourcc, fps, (width, height))

    for idx, frame in enumerate(results):
        if frame.shape[2] == 3:  # Make sure it's not grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        video_writer.write(frame)

        finished_perc = int(idx/len(results)*20)
        print(('\rWRITING FRAMES -> [' + ("="*finished_perc) + (' '*(20-finished_perc)) + ']'), end='')

    print(('\rWRITING FRAMES -> [' + ("="*20) + '] -> COMPLETE'), end='\n') # CLEAR PROGRESS BAR LINE!!!

    # Release the writer
    video_writer.release()

    return save_path+"/"+file_name+".mp4"
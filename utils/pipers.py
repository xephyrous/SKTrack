import os.path

import cv2

def visualize_movie(video_path, save_path, adjusted_fps, inferrer, output, threeDim = False):
    """
    Visualize human skeleton in movie and return point data

    :param video_path: -- path to video file
    :param save_path: -- path to save analyzed video
    :param adjusted_fps: -- video fps to use (0 to use original fps)
    :param inferrer: -- InferMedia | Model to use - model.py
    :param output: -- Console output location
    :param threeDim: -- Analyze people in 3 dimensions | Default False
    :return:
    """
    fps = adjusted_fps if adjusted_fps > 0 else cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)

    output(f"FPS: {round(fps, 2)}")

    if (threeDim):
        results = inferrer.infer_video_three_dim(video_path, return_vis=True, adjusted_fps=fps)
    else:
        results = inferrer.infer_video_two_dim(video_path, return_vis=True, adjusted_fps=fps)

    frames = results[0]

    if len(frames) == 0:
        output("No results", error=True)
        return

    height, width, channels = frames[0].shape

    if not (os.path.exists(save_path)):
        os.makedirs(save_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    inc = 0
    for idx, frame in enumerate(frames):
        if frame.shape[2] == 3:  # Make sure it's not grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        video_writer.write(frame)

        # Slow down visual updates
        if inc == 10:
            inc = 0
            output(f"{int(round((idx/len(frames)) * 100, 1))}% Processed")

        inc += 1
    output("100% Processed")
    # Release the writer
    video_writer.release()

    return save_path, results[1]
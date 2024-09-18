################################################################
#                  I'm new about this stuff.                   #
#   This may be buggy and inefficient as hell, I'm sorry. ;(   #
#                                         - Seuriin            #
################################################################
import cv2
import numpy as np
from tqdm import tqdm 

def interpolate_frame(frame1, frame2, alpha):
    """
    This interpolates a frame between frame1 and frame2 using optical flow.
    (Main)
    """
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # calc optical flow
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    flow = -flow * alpha
    height, width = flow.shape[:2]

    # create a flow map
    flow_map = np.meshgrid(np.arange(width), np.arange(height))
    flow_map = np.stack(flow_map, axis=-1).astype(np.float32)

    # warp the 1st frame using flow
    warped_frame1 = cv2.remap(frame1, flow_map + flow, None, cv2.INTER_LINEAR)

    # blending the warped frame with the second frame based on alpha (-_-)
    interpolated_frame = cv2.addWeighted(warped_frame1, 1 - alpha, frame2, alpha, 0)

    return interpolated_frame

def cfvp(input_video, output_video, target_fps=60):
    cap = cv2.VideoCapture(input_video)
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if not cap.isOpened():
        print(f"Error: Failed to open the video file: {input_video}")
        return

    if target_fps <= input_fps:
        print(f"Error: Target FPS ({target_fps}) must be higher than input FPS ({input_fps})")
        return

    # my simple calc how many interpolated frames are needed per og frame
    interpolation_factor = target_fps / input_fps
    num_interpolated_frames = int(interpolation_factor) - 1

    print(f"Original FPS: {input_fps}, Target FPS: {target_fps}")
    print(f"Inserting {num_interpolated_frames} interpolated frames per original frame.")

    # videowriter setup to save the vid output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, target_fps, (width, height))

    ret, prev_frame = cap.read()
    if not ret:
        print("Failed to read the first frame. :(")
        return

    # tqdm progress bar
    with tqdm(total=frame_count - 1, desc="Processing Video", unit="frames") as pbar:
        for _ in range(frame_count - 1):
            ret, next_frame = cap.read()
            if not ret:
                break

            # wrt original frame
            out.write(prev_frame)

            # generate and write orig frame
            for i in range(1, num_interpolated_frames + 1):
                alpha = i / (num_interpolated_frames + 1)
                interpolated_frame = interpolate_frame(prev_frame, next_frame, alpha)
                out.write(interpolated_frame)

            # move to the next frame
            prev_frame = next_frame
            pbar.update(1)

    # will write the last frame and clean it all up
    out.write(prev_frame)
    cap.release()
    out.release()
    print(f"Video conversion completed: {output_video}")

if __name__ == "__main__":
    # FPS (60, 90, 120, etc.) 
    cfvp('inp.mp4', 'out.mp4', target_fps=90)

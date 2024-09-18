# VD_000001

This Python script uses optical flow to interpolate frames in a video, increasing its frame rate. It reads an input video, generates intermediate frames, and outputs a higher frame rate video. (opencv)

## Features

- Converts a video to a higher FPS using frame interpolation.
- Uses optical flow to estimate intermediate frames.
- Includes a progress bar for tracking progress.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- tqdm

You can install the required packages using pip:

```bash
pip install opencv-python numpy tqdm
```

## Usage

1. **Set up your input and output paths.**
2. **Specify the target FPS for the output video.**

Replace `'inp.mp4'` and `'out.mp4'` with your input and output video file paths, and set your desired frame rate.

```python
if __name__ == "__main__":
    # FPS (60, 90, 120, etc.)
    cfvp('inp.mp4', 'out.mp4', target_fps=90)
```

## Functions

### `interpolate_frame(frame1, frame2, alpha)`

Interpolates a frame between `frame1` and `frame2` using optical flow.

- **frame1**: The first frame (numpy array).
- **frame2**: The second frame (numpy array).
- **alpha**: Interpolation factor between 0 and 1.

Returns the interpolated frame.

### `cfvp(input_video, output_video, target_fps=60)`

Converts a video to a higher FPS by generating intermediate frames.

- **input_video**: Path to the input video.
- **output_video**: Path to save the output video.
- **target_fps**: Target FPS (can be 60, 90, 120, etc.).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

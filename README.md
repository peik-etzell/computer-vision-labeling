## Prerequisites:

```pip install opencv-python numpy ```

Go and download the following files from the internet:
1. `yolov3.weights`   (> 200 MB)
1. `yolov3.cfg`
1. `coco.names`

And put them in the folder called `./.yolo_files/` with the same names as above.

## Running: 

#### Image labeling:

Put images in a folder called ./images/ and run:

`python image_yolo.py`

#### Video labeling:

Put .mp4 videos in a folder called ./videos/ and run:

`python video_yolo.py`

Using YOLOv3 to label images and videos

## Prerequisites:

```pip install opencv-python numpy ```

Go and download the following files from the internet:
1. [`yolov3.weights`](https://pjreddie.com/media/files/yolov3.weights)   (> 200 MB)
1. [`yolov3.cfg`](https://opencv-tutorial.readthedocs.io/en/latest/_downloads/10e685aad953495a95c17bfecd1649e5/yolov3.cfg)
1. [`coco.names`](https://opencv-tutorial.readthedocs.io/en/latest/_downloads/a9fb13cbea0745f3d11da9017d1b8467/coco.names)

And put them in the folder called `./.yolo_files/` with the same names as above.

## Running: 

#### Image labeling:

Put images in a folder called ./images/ and run:

`python image_yolo.py`

#### Video labeling:

Put .mp4 videos in a folder called ./videos/ and run:

`python video_yolo.py`

#### Output:

Labeled videos/images will be put beside the originals in `./images/` and `./videos/`

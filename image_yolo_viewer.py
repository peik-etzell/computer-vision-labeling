# YOLO object detection
import os
import cv2
import numpy as np
import time

WHITE = (255, 255, 255)
img = None
img0 = None
outputs = None

# Load names of classes and get random colors
classes = open('./.yolo_files/coco.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')

# Give the configuration and weight files for the model and load the network.
net = cv2.dnn.readNetFromDarknet(
    './.yolo_files/yolov3.cfg', './.yolo_files/yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# determine the output layer
ln = net.getLayerNames()
# ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# fix from: https://stackoverflow.com/questions/69834335/loading-yolo-invalid-index-to-scalar-variable
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


def load_image(path):
    global img, img0, outputs, ln

    img0 = cv2.imread(path)
    img = img0.copy()

    blob = cv2.dnn.blobFromImage(
        img, 1/255.0, (416, 416), swapRB=True, crop=True)

    net.setInput(blob)
    t0 = time.time()
    outputs = net.forward(ln)
    t = time.time() - t0

    # combine the 3 output groups into 1 (10647, 85)
    # large objects (507, 85)
    # medium objects (2028, 85)
    # small objects (8112, 85)
    outputs = np.vstack(outputs)

    post_process(img, outputs, 0.5)
    cv2.imshow('window',  img)
    cv2.displayOverlay('window', f'forward propagation time={t:.3}')
    cv2.waitKey(0)


def post_process(img, outputs, conf):
    H, W = img.shape[:2]

    numCars = 0

    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        scores = output[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        if confidence > conf:
            x, y, w, h = output[:4] * np.array([W, H, W, H])
            p0 = int(x - w//2), int(y - h//2)
            p1 = int(x + w//2), int(y + h//2)
            boxes.append([*p0, int(w), int(h)])
            confidences.append(float(confidence))
            classIDs.append(classID)
            # print(classes[classID])
            if classes[classID] == 'car':
                numCars += 1
            # cv.rectangle(img, p0, p1, WHITE, 1)

    print('Number of cars: ', numCars)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf, conf-0.1)
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in colors[classIDs[i]]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
            cv2.putText(img, text, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


def trackbar(x):
    global img
    conf = x/100
    img = img0.copy()
    post_process(img, outputs, conf)
    cv2.displayOverlay('window', f'confidence level={conf}')
    cv2.imshow('window', img)


cv2.namedWindow('window')
cv2.createTrackbar('confidence', 'window', 50, 100, trackbar)

dir = './images'
for file in os.listdir(dir):
    print(file)
    load_image(f'{dir}/{file}')
if len(os.listdir(dir)) == 0:
    print('Put your images in "./images/"')

cv2.destroyAllWindows()

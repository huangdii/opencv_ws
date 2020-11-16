from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet

def laneDetection(img):
    img2 = np.copy(img)
    img2 = cv2.bilateralFilter(img2, 5, sigmaColor=5, sigmaSpace=5)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.Canny(img2, 200, 300)
    height, width = img2.shape[:2]
    pt1 = (width*0.45, height*0.62)
    pt2 = (width*0.55, height*0.62)
    pt3 = (width, height*0.9)
    pt4 = (0, height*0.9)
    roi_corners = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)
    if len(img2.shape) == 2:
        channels = 1
    else:
        channels = img2.shape[2]
    mask = np.zeros((height, width), np.uint8)
    ignore_mask_color = (255,) * channels
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    img2 = cv2.bitwise_and(img2, mask)
    lines = cv2.HoughLinesP(img2, 1, np.pi/180, 10, minLineLength=10, maxLineGap=50)
    
    img2 = np.copy(img)
    if len(img2.shape) == 2:
        img2 = cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            cv2.line(img2, (x1, y1), (x2, y2), (0, 0, 255), 3)
    #img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    return img2


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
    return img


netMain = None
metaMain = None
altNames = None


def YOLO():

    global metaMain, netMain, altNames
    configPath = "./cfg/yolov3-tiny-kitti.cfg"
    weightPath = "../Downloads/yolov3-tiny-kitti_last.weights"
    metaPath = "./cfg/darknet_kitti_vm.data"
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("../OpenCV_in_Ubuntu/Data/Lane_Detection_Videos/solidWhiteRight.mp4")
    cap.set(3, 1280)
    cap.set(4, 720)
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
        (darknet.network_width(netMain), darknet.network_height(netMain)))
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    while True:
        prev_time = time.time()
        ret, frame_read = cap.read()
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
        img2 = laneDetection(frame_resized)
        image = cvDrawBoxes(detections, frame_resized)
        image = cv2.addWeighted(img2, 0.5, image, 0.5, 0)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(1/(time.time()-prev_time))
        cv2.imshow('Demo', image)
        cv2.waitKey(3)
    cap.release()
    out.release()

if __name__ == "__main__":
    YOLO()

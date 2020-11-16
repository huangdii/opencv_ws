#!/bin/bash
./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg bin/yolov3-tiny.weights "v4l2src device=/dev/video0 ! video/x-raw, width=640, height=360, format=(string)YUY2,framerate=30/1 ! videoconvert ! video/x-raw,width=640,height=360,format=BGR ! appsink" -thresh 0.2

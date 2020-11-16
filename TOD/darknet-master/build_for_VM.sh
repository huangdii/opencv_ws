#!/bin/bash
sudo apt-get update
sudo apt-get install -y \
 gstreamer1.0-tools gstreamer1.0-alsa \
 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
 gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
 gstreamer1.0-libav \
 libgstreamer1.0-dev \
 libgstreamer-plugins-base1.0-dev \
 libgstreamer-plugins-good1.0-dev \
 libgstreamer-plugins-bad1.0-dev \
 cmake libgflags-dev v4l-utils pyqt5-dev-tools
pip3 install scikit-image
mv Makefile_VM Makefile && make && mkdir bin && cd bin && wget https://pjreddie.com/media/files/yolov3-tiny.weights&& wget https://pjreddie.com/media/files/yolov3.weights && cp yolov3.weights ../
cd .. && git clone https://github.com/JinFree/labelImg.git && \
cd labelImg && \
sudo pip3 install -r requirements/requirements-linux-python3.txt && \
make qt5py3

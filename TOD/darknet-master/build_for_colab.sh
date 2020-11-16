#!/bin/bash
echo "export PATH=/usr/local/cuda-10.0/bin:\$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:\$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc
sudo apt-get install -y cmake libgflags-dev
mv Makefile_colab Makefile && make && mkdir bin && cd bin && wget https://pjreddie.com/media/files/yolov3-tiny.weights && wget wget https://pjreddie.com/media/files/darknet53.conv.74

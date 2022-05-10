# Annotation-app
Annotations selection app using PyQt5 wich deals with the annotations of COCO dataset.
The idea is to select a suitable annotation from each image and save its index in a json file, then inpaint these images with Shiftmap and Navier-Stoks methods

The output:
1) json file with a dictionary (image name is the key & the index of the selected annotation is the value).
2) Inpainted images with both Shiftmap and Navier-Stoks methods

Dependencies:
1) git clone https://github.com/pdollar/coco.git
2) pip install pyqt5-tools

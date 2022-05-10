# Annotation-app
Annotations selection app using PyQt5 wich deals with the annotations of COCO dataset.
The idea is to select an annotation from the image and save its index in a json file, then inpaint these images with Shiftmap and Navier-Stoks methods
This json file has a dictionary (image name is the key & the index of the annotation is the value).

Dependencies:
1) git clone https://github.com/pdollar/coco.git
2) pip install pyqt5-tools

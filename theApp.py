# to build it --> pyinstaller.exe --onefile --windowed --icon=logo.ico theApp.py

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui, QtWidgets
from pycocotools.coco import COCO
from PIL import Image, ImageQt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5 import QtCore 
from os import path
import numpy as np
import threading
import random
import json
import sys
import cv2
import os

class MainApp(QMainWindow):
    
    coco = ""
    jsonFilePath = "" # json file that we will save in
    annsFolderPath = "" # json file that has the annotations
    imagesFolderPath = ""
    data = {} # Dictionary that holds the index of the selected annotation in each image 
    theMasks = [] # Array to append the masks of the selected image in it
    saftySave = 0 # Counter to save automatically every 20 images
    picPointer = -1 # Iterable pointer to the contents of the folder

    def __init__(self):
        
        super(MainApp , self).__init__()
        loadUi("mainWindow.ui", self)
        self.Buttons()
        self.initialization()
    
    
    def initialization(self):

        self.skip.setValidator(QIntValidator())
        self.nextButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.backButton.setEnabled(False)
        self.inpaintButton.setEnabled(False)
        self.forwardButton.setEnabled(False)
        self.backwardButton.setEnabled(False)
        self.actionInpaint.setEnabled(False)
        self.imageName.clear()
        self.photo.clear()
        self.shiftmap.clear()
        self.navier.clear()
        self.listWidget.clear()
        self.lineEdit1.clear()
        self.lineEdit2.clear()
        self.skip.setText("0")
        self.extension.setText(".jpg")
        self.startButton.setEnabled(True)
        self.browseButton1.setEnabled(True)
        self.browseButton2.setEnabled(True)
        self.extension.setEnabled(True)
        self.lineEdit1.setEnabled(True)
        self.lineEdit2.setEnabled(True)

    # Handle all button actions
    def Buttons(self):

        self.browseButton1.clicked.connect(self.browseAnns)
        self.browseButton2.clicked.connect(self.browseImages)
        self.startButton.clicked.connect(self.Starting)
        self.nextButton.clicked.connect(self.nextPic)
        self.saveButton.clicked.connect(self.save)
        self.backButton.clicked.connect(self.back)
        self.inpaintButton.clicked.connect(self.navierInpaint)
        self.listWidget.itemClicked.connect(self.highlightMask)
        self.resetButton.clicked.connect(self.reset)
        self.exitButton.clicked.connect(self.exit)
        self.forwardButton.clicked.connect(self.skipForward)
        self.backwardButton.clicked.connect(self.skipBackward)
        self.actionInpaint.triggered.connect(self.toSecondScreen)
        self.actionDefault_size.triggered.connect(self.defaultSize)

    def defaultSize(self):
        
        if widget.width() != int(dw.width()*0.8) or widget.height() != int(dw.height()*0.8):
            self.photo.clear()
            self.navier.clear()
            self.shiftmap.clear()
            self.listWidget.clear()
            self.showmessagebox("Information", "Please wait. :)")
            widget.resize(x,y)
            if not self.startButton.isEnabled(): # Check if the program starts or not
                self.picPointer -= 1
                self.nextPic()
        else:
            pass
        
    def skipForward(self):
        if not self.skip.text():
            self.showmessagebox("Invalid input", "Please enter a number")

        elif int(self.skip.text()) < 0:
            self.showmessagebox("Invalid input", "Please enter a positive number")
        
        else:
            self.picPointer += int(self.skip.text())
            self.nextPic()


    def skipBackward(self):
        if not self.skip.text():
            self.showmessagebox("Invalid input", "Please enter a number")

        elif int(self.skip.text()) < 0:
            self.showmessagebox("Invalid input", "Please enter a positive number")
        
        else:
            self.picPointer -= int(self.skip.text()) + 2
            self.nextPic()


    def toSecondScreen(self):
        self.saveInFile()
        second.lineEdit.setText(self.imagesFolderPath)
        second.lineEdit0.setText(self.annsFolderPath)
        second.skipCheckBox.setChecked(True)
        second.lineEdit1.setText(self.jsonFilePath)
        second.imagesExtension = self.extension.text()
        widget.setCurrentIndex(widget.currentIndex() + 1) # Move forward to second screen in the stack
        
    def showmessagebox(self, title, message):

        msgbox = QMessageBox()
        msgbox.resize(300,200)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle(title)
        msgbox.setText(message)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()

    # Get the annotations file path
    def browseAnns(self):

        fname = QFileDialog.getOpenFileName(self, "Select the annotations file", "D:/FCIH/GraduationProject/Dataset", "(*.json)")
        self.lineEdit1.setText(fname[0])
    
    # Get the images folder path
    def browseImages(self):

        folderDirectory = QFileDialog.getExistingDirectory(self, "Select the images folder", "D:/FCIH/GraduationProject/Dataset")
        self.lineEdit2.setText(folderDirectory)


    # Starting point after clicking on Start button
    def Starting(self):
        
        check1 = os.path.isfile(self.lineEdit1.text())
        check2 = os.path.isdir(self.lineEdit2.text())
        if check1 and check2:
            self.annsFolderPath = self.lineEdit1.text()
            self.imagesFolderPath = self.lineEdit2.text()
            self.coco = COCO(self.annsFolderPath)
            # print(self.coco)
            
            if len(os.listdir(self.imagesFolderPath)) != 0:

                if self.extension.text() in os.listdir(self.imagesFolderPath)[0]:
                    self.startButton.setEnabled(False)
                    self.browseButton1.setEnabled(False)
                    self.browseButton2.setEnabled(False)
                    self.extension.setEnabled(False)
                    self.lineEdit1.setEnabled(False)
                    self.lineEdit2.setEnabled(False)
                    self.nextButton.setEnabled(True)
                    self.saveButton.setEnabled(True)
                    self.backButton.setEnabled(True)
                    self.inpaintButton.setEnabled(True)
                    self.forwardButton.setEnabled(True)
                    self.backwardButton.setEnabled(True)
                    self.actionInpaint.setEnabled(True)
                    self.nextPic()
                else:
                    self.showmessagebox("Error", "There are images with worng extension in this folder")
            else:
                self.showmessagebox("Warning!", "This folder is empty")
        
        else:
            self.showmessagebox("Error", "Please check your paths and try again")
            


    # Display the image and its masks
    def nextPic(self):
        print(self.picPointer)
        self.picPointer += 1
        
        # make boundaries to the pointer to avoid out of range problem
        if self.picPointer >= len(os.listdir(self.imagesFolderPath)):
            self.picPointer = len(os.listdir(self.imagesFolderPath)) - 1
            self.showmessagebox("Invalid command", "No data to show!\nThis is the end of the folder")
        elif self.picPointer <= -1:
            self.picPointer = 0
            self.showmessagebox("Invalid command", "No data to show!\nThis is the start of the folder")
        
        self.theMasks = []
        self.photo.clear()
        self.shiftmap.clear()
        self.navier.clear()
        self.listWidget.clear()
        
        image = os.listdir(self.imagesFolderPath)[self.picPointer]
        if self.extension.text() in image:
            image_id = int(image.removesuffix(self.extension.text()).lstrip('0'))
            
            annotationIDs = self.coco.getAnnIds(image_id) #Get ann ids that satisfy given filter conditions.
            if len(annotationIDs) > 0:

                annotations = self.coco.loadAnns(annotationIDs) #Load anns with the specified ids.
                #annotaitions variable is a list of dictionaries, each dectionary is for an object
                pixmap_image = QtGui.QPixmap(self.imagesFolderPath + "/" + image).scaled(self.photo.width(), self.photo.height(), QtCore.Qt.KeepAspectRatio)
                self.photo.setPixmap(pixmap_image) # Display the image in the label
                self.imageName.setText(image)
                
                annIndex = 0 
                for ann in annotations:
                    mask = self.coco.annToMask(ann)
                    self.theMasks.append(mask) # Save masks in an array to retrieve them easily
                    mask = 1 - mask 
                    mask_img = Image.fromarray((mask * 255).astype(np.uint8))
                    qtImage = ImageQt.ImageQt(mask_img) # convert Image to ImageQt
                    qMask = QtGui.QPixmap.fromImage(qtImage)
                    icon = QtGui.QIcon(qMask)
                    item = QtWidgets.QListWidgetItem(icon, f"{ann['id']}")
                    self.listWidget.addItem(item)
                    annIndex += 1

                # Automatically save every 20 images
                self.saftySave += 1
                if self.saftySave >= 20:
                    self.saveInFile()
                    self.saftySave = 0
            else:
                self.showmessagebox("Warning!", "This annotations file has missing data")
        else:
            self.showmessagebox("Error", f"Image \"{image}\" has wrong extension\nPress reset and make sure of extensions.\nThe saved data will not be lost. :)")

    def back(self):

        if self.picPointer <= 0:
            self.showmessagebox("Invalid command", "No data to show!")
        else:
            self.picPointer -= 2
            self.nextPic()

    def navierInpaint(self):

        if not self.listWidget.currentItem():
            self.showmessagebox("Invalid command", "Please select a mask.")
            
        else:
            originalMask = self.theMasks[self.listWidget.currentRow()]
            originalImage = cv2.imread(self.imagesFolderPath + "/" + self.imageName.text())
            if self.checkBox.isChecked():
                t1 = threading.Thread(target = self.shiftMapInpaint, args = (originalImage, originalMask))
                t1.start()
                self.setEnabled(False)
                self.shiftmap.setText("Please Wait...")
                
            image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB) 
            NS = cv2.inpaint(image, originalMask, 3, cv2.INPAINT_NS)

            # Convert np image to QPixmap 
            height, width, _ = NS.shape
            qImage = QImage(NS.data, width, height, 3 * width, QImage.Format_RGB888)
            pixmapImg = QtGui.QPixmap.fromImage(qImage).scaled(self.navier.width(), self.navier.height(), QtCore.Qt.KeepAspectRatio)
            self.navier.setPixmap(pixmapImg)

    def shiftMapInpaint(self, img, msk):
        
        # zero --> 255 & 1 --> zero
        maskInv = 1 - msk
        maskInv = maskInv * 255

        SHIFTMAP = np.zeros_like(img)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        
        # Expand the mask
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (2 * 3 + 1, 2 * 3 + 1))
        maskInv = cv2.erode(maskInv, element)

        cv2.xphoto.inpaint(image, maskInv, SHIFTMAP, cv2.xphoto.INPAINT_SHIFTMAP)
        SHIFTMAP = cv2.cvtColor(SHIFTMAP, cv2.COLOR_Lab2RGB)

        # Convert np image to QPixmap 
        height, width, _ = SHIFTMAP.shape
        qImage = QImage(SHIFTMAP.data, width, height, 3 * width, QImage.Format_RGB888)
        pixmapImg = QtGui.QPixmap.fromImage(qImage).scaled(self.shiftmap.width(), self.shiftmap.height(), QtCore.Qt.KeepAspectRatio)
        self.shiftmap.clear() # Clear (Please wait...) sentence
        self.setEnabled(True)
        self.shiftmap.setPixmap(pixmapImg)

    # saving the image ID and the index of the selected annotation
    def save(self):
        
        # First save
        if len(self.jsonFilePath) == 0: 
            fname = QFileDialog.getOpenFileName(self, "Select json file for saving data", "D:/FCIH/GraduationProject/Dataset", "(*.json)")
            self.jsonFilePath = fname[0]

            # if this json file has data
            try:
                with open(self.jsonFilePath, 'r') as f:
                    self.data = json.load(f) # Get the data to append to it
            except:
                pass

        else:

            if self.listWidget.currentItem():
                annotationID = int(self.listWidget.currentItem().text())            
                self.data[self.imageName.text()] = annotationID    
                print(self.data)            
                self.nextPic()
            else:
                self.showmessagebox("Invalid command", "Please select a mask.")

    # Highlight the selected object
    def highlightMask(self):
        
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        mask = self.theMasks[self.listWidget.currentRow()]
        image = cv2.imread(self.imagesFolderPath + "/" + self.imageName.text())

        # Create colored mask
        colored = np.zeros(image.shape, image.dtype)
        colored[:,:] = (r, g, b)
        redMask = cv2.bitwise_and(colored, colored, mask = mask)
        npImage = cv2.addWeighted(redMask, 1, image, 1, 0, image)

        # Convert np image to QPixmap
        height, width, _ = npImage.shape
        qImg = QImage(npImage.data, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()

        # Display the new image with the highlited object
        self.photo.setPixmap(QtGui.QPixmap.fromImage(qImg).scaled(self.photo.width(), self.photo.height(), QtCore.Qt.KeepAspectRatio))

    # Save the current dictionary values in the json file 
    def saveInFile(self):
        try:
            with open(self.jsonFilePath, 'w') as f:
                json.dump(self.data, f)
        except:
            pass # There is no josn file to save in

    def reset(self):

        self.saveInFile()
        self.jsonFilePath = ""
        self.picPointer = -1 # Iterable pointer to the contents of the folder
        self.saftySave = 0
        self.data = {} 
        self.initialization()
    
    def exit(self):

        self.saveInFile()
        widget.close()



class screen2(QMainWindow):

    loop = None
    coco = ""
    data = {}
    shiftFlag = 0
    func = []
    imagesExtension = ""
    
    def __init__(self):
        
        super(screen2, self).__init__()
        loadUi("screen2.ui", self)
        self.Buttons()

    def Buttons(self):
        self.browseJson.clicked.connect(self.selectJson)
        self.containsButton.clicked.connect(self.numberOfItems)
        self.browseShift.clicked.connect(self.shiftDestination)
        self.browseNavier.clicked.connect(self.navierDestination)
        self.startInpaint.clicked.connect(self.start)
        self.backToMain.clicked.connect(lambda self: widget.setCurrentIndex(widget.currentIndex() - 1))# Move backward to previous screen in the stack
        self.skipCheckBox.setChecked(True)

    # Retrieve number of the items in the json file
    def numberOfItems(self):
        retrievedData = {}
        if self.lineEdit1.text() and os.path.isfile(self.lineEdit1.text()):
            try:
                with open(self.lineEdit1.text(), 'r') as f:
                    retrievedData = json.load(f) # Get the data to append to it
            except:
                pass
            
            MainApp.showmessagebox(self, "Inforamtion", f"This json file contains {len(retrievedData)} items")
        else:
            MainApp.showmessagebox(self, "Error", "Invalid path")    
     

    def selectJson(self):

        fileDirectory = QFileDialog.getOpenFileName(self, "Select the json file", "D:/FCIH/GraduationProject/Dataset", "(*.json)")
        self.lineEdit1.setText(fileDirectory[0])

    # Selecting the destination folder that will hold the shiftmap data
    def shiftDestination(self): 

        folderDirectory = QFileDialog.getExistingDirectory(self, "Select the desitnation folder", "D:/FCIH/GraduationProject/Dataset")
        self.lineEdit2.setText(folderDirectory)

    # Selecting the destination folder that will hold the navier data
    def navierDestination(self): 

        folderDirectory = QFileDialog.getExistingDirectory(self, "Select the desitnation folder", "D:/FCIH/GraduationProject/Dataset")
        self.lineEdit3.setText(folderDirectory)

    def start(self):
        
        check1 = os.path.isfile(self.lineEdit1.text()) # Check for the path of json file
        check2 = os.path.isdir(self.lineEdit2.text()) # Check if the path of the shiftmap destination folder exists
        check3 = os.path.isdir(self.lineEdit3.text()) # Check if the path of the navier destination folder exists
        if check1 and (check2 or check3):
            self.inpainting()
            
        else:
            MainApp.showmessagebox(self, "Error", "Please make sure from your paths!")

    def inpainting(self):

        jsonCheck = 1
        allImages = []
        allMasks = []
        names = []
        try:
            with open(self.lineEdit1.text(), 'r') as f:
                self.data = json.load(f) # Get the data to append to it
        except:
            jsonCheck = 0
            
        if jsonCheck and len(self.data) != 0:
            
            self.coco = COCO(self.lineEdit0.text()) # lineEdit0 --> annotations directory 
            for image in self.data:
                if self.imagesExtension in image: # Check for the right extension to avoid json files with different image extensions
                    if os.path.isfile(self.lineEdit.text() + "/" + image): # To check first if the image is found in this folder or not
                        originalImage = cv2.imread(self.lineEdit.text() + "/" + image) # lineEdit --> images directory 
                        ann = self.coco.loadAnns(self.data[image]) 
                        #type of ann is (list), which has only one item, because we specified the annotation id
                        
                        mask = self.coco.annToMask(ann[0])

                        # Saving name of the image, the image itself, and its mask to loop over them in inpainting methods
                        allImages.append(originalImage)
                        allMasks.append(mask)
                        names.append(image)
                    else:
                        continue # Ignore the images that are found in the json file and not found in the images folder 
                else:
                    MainApp.showmessagebox(self, "Error", "Wrong extensions are found in this json file!")
                    return
            
            threads = []
            if self.lineEdit2.text():
                t1 = threading.Thread(target = self.shiftMapInpaint, args = (allImages, allMasks, names))
                t1.start()
                threads.append(t1)

            if self.lineEdit3.text():
                t2 = threading.Thread(target = self.navier, args = (allImages, allMasks, names))
                t2.start()
                threads.append(t2)

            widget.setEnabled(False)
            MainApp.showmessagebox(self, "Information", "This may take some time please wait")
            for thread in threads:
                thread.join()
                
            MainApp.showmessagebox(self, "Information", "Inpainted process ended successfully")
            widget.setEnabled(True)

        else:
            MainApp.showmessagebox(self, "Warning", "This json file has no data!")

    def shiftMapInpaint(self, images, masks, names):
        
        for (img, msk, name) in zip(images, masks, names):
            print("shiftmap")
            if self.skipCheckBox.isChecked() and os.path.isfile(self.lineEdit2.text() + "/" + name):
                continue

            else:
                maskInv = 1 - msk
                maskInv = maskInv * 255

                SHIFTMAP = np.zeros_like(img)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
                
                # Expand the mask
                element = cv2.getStructuringElement(cv2.MORPH_CROSS, (2 * 3 + 1, 2 * 3 + 1))
                maskInv = cv2.erode(maskInv, element)

                cv2.xphoto.inpaint(img, maskInv, SHIFTMAP, cv2.xphoto.INPAINT_SHIFTMAP)
                SHIFTMAP = cv2.cvtColor(SHIFTMAP, cv2.COLOR_Lab2RGB)
                cv2.imwrite(self.lineEdit2.text() + "/" + name, SHIFTMAP) # lineEdit2 --> shiftmap destination folder

    def navier(self, images, masks, names):

        for (img, msk, name) in zip(images, masks, names):
            print("navier")
            if self.skipCheckBox.isChecked() and os.path.isfile(self.lineEdit3.text() + "/" + name):
                continue
            else:
                NS = cv2.inpaint(img, msk, 3, cv2.INPAINT_NS)
                cv2.imwrite(self.lineEdit3.text() + "/" + name, NS) # lineEdit3 --> Navier destination folder

if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    window = MainApp()
    second = screen2()
    dw = QDesktopWidget() 

    # Default size
    x = int(dw.width()*0.8)
    y = int(dw.height()*0.8)
    widget.resize(x, y)

    widget.setWindowTitle("AnnApp")
    widget.setWindowIcon(QtGui.QIcon('logo.ico'))
    widget.addWidget(window)
    widget.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
    widget.show()
    widget.addWidget(second) # Add the second screen to the stack

    app.exec_()

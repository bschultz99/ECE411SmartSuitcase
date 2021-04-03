#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
#idea
#put everything in a try except to make it more robust? so it basically autorestarts itself
#while True
#  try
    #code
    #break
    #excpet
    #close windows and capture basically sending it into restart

#We will use the coco dataset as it is very popular and gives us the ability to track some items that we are interested in
#utilizing opencv version 4.5.1
#cocodataset.org

coco_names='coco.names'
classes=[]
with open(coco_names,'rt') as f: # read in all of the coco classes that we can detect from the file
    for line in f:
        currentPlace = line[:-1]
        classes.append(currentPlace)

configPath='ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath='frozen_inference_graph.pb'

model =cv2.dnn_DetectionModel(weightsPath,configPath) #instantiate the detection object we will use and pass in the information it will need
model.setInputSize(320,320) #set the size of the input width = height = 320
model.setInputMean((127.5,127.5,127.5)) #sets the mean value for a frame which is subtracted from channels
model.setInputSwapRB(True) #switch the red and blue color channels in the tensors
model.setInputScale(1.0/127.5) #sets the scalefactor for a frame this is a scale multiplier for frames
#values are standard values I saw in various examples


#cap = cv2.VideoCapture(0)
#cap.set(3,640) #set the width of the capture
#cap.set(4,480) #set the height of the capture
#cap.set(10,80) #adjust brightness
camera=PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(640,480))
time.sleep(.2) #allow camera to warm up


for image in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    frame = image.array
    #success, frame = cap.read()
    classification, confidence, bbox = model.detect(frame, confThreshold=.45) #classify something in the capture if it is 65% confident or better
    #get the classification of an object with what confidence and get the bounding box around it
    #the bounding box will be the information that we use to make decisions
    if len(classification)!=0:
#     if True:
        for obj, conf, bbox in zip(classification.flatten(),confidence.flatten(), bbox): #flatten compresses the matrix into a 1D based on contiguous row major order
            #zip groups up coressponding elements in the 3 iterables of interest
            cv2.rectangle(frame,bbox, color=(255,0,0), thickness=2) #draw a box around the objects that we want
            cv2.putText(frame,classes[obj-1],(bbox[0]+10,bbox[1]+30), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), thickness=3) #write the classification into the box
            if classes[obj-1]=="frisbee" or classes[obj-1]=="remote" or classes[obj-1]=="toothbrush":
#                 centerpoint=(int(bbox[0]+(bbox[2]-bbox[0])/2),int(bbox[1]+(bbox[3]-bbox[1])/2))
                centerpoint=(int(bbox[0]+(bbox[2])/2),int(bbox[1]+(bbox[3])/2))
                if centerpoint[0]<310:
                    print('left')
                if centerpoint[0]>330:
                    print('right')
                
                cv2.circle(frame,centerpoint,10,(0,0,255),-1)
    cv2.line(frame,(320,0),(320,480),(255,0,0),3) #draw the center line
    #potentially implement a deadzone?
    
    cv2.imshow("tracking", frame) #actually display the video
    #prepare for the next frame
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'): #quit if q is pressed MIGHT NEED TO CHANGE ON RAPSBERRY PI BECAUSE NOT A 64 BIT MACHINE
        break
#cap.release() #release the capture
cv2.destroyAllWindows() #destroy the capture window that was created


#I learned about these OpenCV features primarily from the documentation and from Murtaza's Workshop video https://www.youtube.com/watch?v=HXDD7-EnGBY
        


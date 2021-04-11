from picamera import PiCamera
import cv2
import time
from picamera.array import PiRGBArray

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





camera=PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(640,480))
time.sleep(.1)
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    image=frame.array
    classification, confidence, bbox = model.detect(image, confThreshold=.45)
    
    if len(classification)!=0:
#     if True:
        for obj, conf, bbox in zip(classification.flatten(),confidence.flatten(), bbox): #flatten compresses the matrix into a 1D based on contiguous row major order
            #zip groups up coressponding elements in the 3 iterables of interest
            cv2.rectangle(image,bbox, color=(255,0,0), thickness=2) #draw a box around the objects that we want
            cv2.putText(image,classes[obj-1],(bbox[0]+10,bbox[1]+30), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), thickness=3) #write the classification into the box
            if classes[obj-1]=="frisbee" or classes[obj-1]=="remote" or classes[obj-1]=="toothbrush":
#                 centerpoint=(int(bbox[0]+(bbox[2]-bbox[0])/2),int(bbox[1]+(bbox[3]-bbox[1])/2))
                centerpoint=(int(bbox[0]+(bbox[2])/2),int(bbox[1]+(bbox[3])/2))
                if centerpoint[0]<310:
                    print('left')
                if centerpoint[0]>330:
                    print('right')
                
                cv2.circle(image,centerpoint,10,(0,0,255),-1)
    
    
    
    cv2.line(image,(320,0),(320,480),(255,0,0),3)
    cv2.imshow("Frame",image)
    key=cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
    


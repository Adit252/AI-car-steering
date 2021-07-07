# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:43:53 2020

@author: Aditya Khandelwal
"""
import cv2
import numpy as np
import math
from pynput.keyboard import Key, Controller


#Setting up the webcam
wc = cv2.VideoCapture(0)
wc.open(0)
wc.set(3,640)       #width
wc.set(4,480)       #height
wc.set(10,150)

my_colors = [ [120, 120, 0, 160, 255, 255],
             [15, 140, 130, 90, 255, 255] ]    #writing all the trackbar values of different colors

myColorValues = [[0, 0, 255],                          #BGR FORMAT
                 [0, 0, 255]]

myPoints = []                     #[x, y, colorID]

keyboard = Controller()
flag = 1

def getAngle(a, b, c):
   ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
   return ang + 360 if ang < 0 else ang

def findcolor(image, my_colors, mycolorvalues):
    
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                       #hue saturation value model, make it easy to make color adjustments
    count = 0
    newpoints = []
    for color in my_colors:    
    
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult, (x,y + 25), 10, mycolorvalues[count], cv2.FILLED)
        #cv2.line(imgResult, (x,y + 25 ),(image.shape[1], y + 25), (0,255,0), 3)
        #cv2.line(imgResult, (x,y + 25 ),(x, y + 25), (0,255,0), 3)
        
        if x!= 0 and y!= 0 : newpoints.append([x, y, count])
        count += 1
        #cv2.imshow(str(color[0]), mask)                   # we have randomly assignned name so as to get diff. colors
    if len(newpoints) == 2 :
        cv2.line(imgResult, (x,y + 25 ),(image.shape[1], y + 25), (0,255,0), 3)
        cv2.line(imgResult, (newpoints[0][0],newpoints[0][1] + 25 ),(newpoints[1][0], newpoints[1][1] + 25), (0,255,0), 3)
        c3 = [image.shape[1] ,newpoints[1][1]]
        angle = getAngle(newpoints[0], newpoints[1], c3)
        angle = int(angle)
        #print(angle)
        cv2.putText(imgResult, str(angle) + ' degree', (newpoints[1][0] + 40,newpoints[1][1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 0, 0), 1)
        
        keyboard.press(Key.up)
        keyboard.release(Key.up)
        print('UP') 
    
    else : angle = 0
    #print(newpoints)
    return newpoints, angle

def getContours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)    #2nd argument s best for outer 
    x,y,width,height = 0,0,0,0
    for cnt in contours :
        area = cv2.contourArea(cnt)
        if area > 600:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)    #last argument is 3
            peri = cv2.arcLength(cnt, True)             #True means the shape is closed
            
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, width, height = cv2.boundingRect(approx)          #this will give the shape and size of the bounding boxes
    return x + width//2, y

# Read until video is completed
while(wc.isOpened()):
  # Capture frame-by-frame
  ret, image = wc.read()
  image = cv2.flip(image,1)
  imgResult = image.copy()
  if ret == True:

    # Display the resulting frame
    Values = findcolor(image, my_colors, myColorValues)
    thresh = Values[1]                         #calling the functions in the webcam to get all the colors
    newPoints = Values[0]
    
    
    if thresh < 30:     
        flag = 0
        
    if flag == 0 :  
        
        if len(newPoints)!= 0 :
           for point in newPoints:
              myPoints.append(point)    
        
        if thresh > 20 and thresh < 50:
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            print('LEFT') 
            flag = 1
            
        if thresh > 320 and thresh < 350 : 
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            print('RIGHT')
            flag = 1
    
    if thresh > 50 and thresh < 80 :
        keyboard.press(Key.left)
        keyboard.release(Key.left)
        print('LEFT') 
    
    if thresh < 320 and thresh > 270:
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        print('RIGHT')
        
        
    cv2.imshow('Result', imgResult)
    # Press Q on keyboaqrd to  exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  # Break the loop
  else: 
    break

# When everything done, release the video capture object
wc.release()
# Closes all the frames
cv2.destroyAllWindows()




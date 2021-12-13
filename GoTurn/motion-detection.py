from __future__ import print_function
import sys
import cv2
from random import randint
import tensorflow as tf


FILE_OUTPUT = 'output.avi'
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

cap = cv2.VideoCapture("highway.mp4")

# Read first frame
success, frame = cap.read()
frame = cv2.resize(frame, (720, 480),interpolation = cv2.INTER_AREA)

delay_counter = 0

if not success:
  print('Failed to read video')
  sys.exit(1)

## Select boxes
bboxes = []
colors = [] 

def getUserSelections():
    bbox = cv2.selectROI('MultiTracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    print("Press q to quit selecting boxes and start tracking")
    print("Press any other key to select next object")
    


while True:
  getUserSelections()
  k = cv2.waitKey(0) & 0xFF
  print(k)
  if (k == 113):
    break

multiTracker = cv2.MultiTracker_create()

for bbox in bboxes:
  multiTracker.add(cv2.TrackerGOTURN_create(), frame, bbox)
  
timer = cv2.getTickCount()
  
success, boxes = multiTracker.update(frame)

fps = cv2.getTickFrequency() // ((cv2.getTickCount() - timer)*10000)

out = cv2.VideoWriter(FILE_OUTPUT, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                      10, (720, 480))

while True:
  success, frame = cap.read()
  frame = cv2.resize(frame, (720, 480),interpolation = cv2.INTER_AREA)
  
  if not success:
    break

  timer = cv2.getTickCount()
  
  if delay_counter > 2:
  
    success, boxes = multiTracker.update(frame)
    delay_counter = 0
  
  fps = cv2.getTickFrequency() // ((cv2.getTickCount() - timer)*10000)

  for i, newbox in enumerate(boxes):
    p1 = (int(newbox[0]), int(newbox[1]))
    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

  cv2.putText(frame, "GOTURN" + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)
  cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
  out.write(frame)
  cv2.imshow('MultiTracker', frame)
  
  delay_counter = delay_counter + 1
  
  if cv2.waitKey(1) & 0xFF == 27:
    break
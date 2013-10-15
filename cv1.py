import cv2
import cv
import numpy as np
import matplotlib.pyplot as plt

# setup video capture
cap = cv2.VideoCapture('cg30116_20130216_ag_PF24_A_r_1.avi')

frames = []
# get frame, store in array

while True:
    #cap.set(cv.CV_CAP_PROP_POS_FRAMES, 1)
    ret,im = cap.read()
    print(ret)
    cv2.imshow('video',im)
    frames.append(im)
    if cv2.waitKey(10) == 27:
        break
    print(len(frames))


frames = np.array(frames)
print(np.shape(frames))
print('frame', np.shape(frames[0]))
# check the sizes
plt.imshow(frames[0])
plt.savefig('frame0.png')

from PIL import Image
import time
import numpy as np
import cv2

imfile = 'mov0001.jpeg'
START = time.time()
print(START)
x = np.array(Image.open(imfile))
print('Image.open', time.time()-START)
print(np.shape(x))



START = time.time()
print(START)
x = cv2.imread(imfile, 0)
print('cv2', time.time()-START)
print(np.shape(x))
print(type(x))

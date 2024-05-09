import cv2
import numpy as np

image_bgr = cv2.imread("C:/Users/chaoy/Pictures/chaoyi-signature.png")
print(image_bgr.shape)
# get the image dimensions (height, width and channels)
h, w, c = image_bgr.shape
# append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=2)
print(image_bgra.shape)
# create a mask where white pixels ([255, 255, 255]) are True
white = np.all(image_bgr == [255, 255, 255], axis=-1)
print(type(white))
# change the values of Alpha to 0 for all the white pixels
image_bgra[white, -1] = 0
# save the image
cv2.imwrite('C:/Users/chaoy/Pictures/image_bgra.png', image_bgra)
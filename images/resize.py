import cv2

img = cv2.imread('neeraj2.jpg', 1)
img = cv2.resize(img, (96,96), interpolation= cv2.INTER_AREA)
cv2.imwrite('rneeraj2.jpg', img)

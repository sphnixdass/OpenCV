# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2


#https://www.quora.com/How-can-I-detect-an-object-from-static-image-and-crop-it-from-the-image-using-openCV
#https://stackoverflow.com/questions/9413216/simple-digit-recognition-ocr-in-opencv-python

# load the puzzle and waldo images
#imgwork = cv2.imread("ocrsample.JPG")
### loop over varying widths to resize the image to
##for width in (200,200,200,200):
##	# resize the image and display it
##	resized = imutils.resize(imgwork, width=width)
##	cv2.imshow("Width=%dpx" % (width), resized)
	


##gray = cv2.cvtColor(imgwork, cv2.COLOR_BGR2GRAY)
##skeleton = imutils.skeletonize(gray, size=(2, 2))
##cv2.imshow("Skeleton", skeleton)


im = cv2.imread('Pic-d.png')
im3 = im.copy()

#im = imutils.resize(im, height = 300)

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
#thresh = imutils.skeletonize(thresh, size=(3, 3))
#cv2.imshow("blur",blur)
#cv2.imshow("thresh",thresh)

#################      Now finding Contours         ###################

im2, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]
print(len(contours))

idx = 0
for c in contours:
	x,y,w,h = cv2.boundingRect(c)
	if w>30 and h>50:
		idx+=1
		new_img=im[y:y+h,x:x+w]
		cv2.imshow(str(idx) + '.png',new_img)
		#cv2.imwrite(str(idx) + '.png', new_img)
cv2.imshow("im",im)


##for cnt in contours:
##    if cv2.contourArea(cnt)>50:
##        [x,y,w,h] = cv2.boundingRect(cnt)
##        #print("x = " + str(x) + "; y = " + str(y) + "; w = " + str(w) + "; h = " + str(h))
##        if  h>50:
##            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
##            roi = thresh[y:y+h,x:x+w]
##            roismall = cv2.resize(roi,(10,10))
##            cv2.imshow('norm',im)
##            key = cv2.waitKey(0)
##
##            if key == 27:  # (escape to quit)
##                sys.exit()
##            elif key in keys:
##                responses.append(int(chr(key)))
##                sample = roismall.reshape((1,100))
##                samples = np.append(samples,sample,0)
##
##responses = np.array(responses,np.float32)
##responses = responses.reshape((responses.size,1))
##print ("training complete")
##
##np.savetxt('generalsamples.data',samples)
##np.savetxt('generalresponses.data',responses)

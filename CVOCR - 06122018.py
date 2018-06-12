# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
import sys
import os
import csv
from PIL import Image
from numpy import genfromtxt
from sklearn import datasets, svm, metrics

# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.


#https://www.quora.com/How-can-I-detect-an-object-from-static-image-and-crop-it-from-the-image-using-openCV
#https://stackoverflow.com/questions/9413216/simple-digit-recognition-ocr-in-opencv-python

# load the puzzle and waldo images
#imgwork = cv2.imread("ocrsample.JPG")
### loop over varying widths to resize the image to
##for width in (200,200,200,200):
##  # resize the image and display it
##  resized = imutils.resize(imgwork, width=width)
##  cv2.imshow("Width=%dpx" % (width), resized)
    


##gray = cv2.cvtColor(imgwork, cv2.COLOR_BGR2GRAY)
##skeleton = imutils.skeletonize(gray, size=(2, 2))
##cv2.imshow("Skeleton", skeleton)


im = cv2.imread('Pic-d111.png')
im3 = im.copy()
imorg = im.copy()

#im = imutils.resize(im, height = 300)

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
#thresh = imutils.skeletonize(thresh, size=(3, 3))
#cv2.imshow("blur",blur)
#cv2.imshow("thresh",thresh)

#################      Now finding Contours         ###################

im2, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
rc = 1
samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]
print(len(contours))

idx = 0
y2 = 0
for c in contours:
        
    x,y,w,h = cv2.boundingRect(c)
    #if w>40 and h>50:
    #print(y2-y)
    
    
    #if w>30 and h>40 and h<100 and (y2-y) > 3:
    if w>30 and h>40 and h<90 and (y2-y) > 3:
    #if idx >=0:
                imtemp = imorg.copy()
                cv2.rectangle(imtemp,(x,y),(x+w,y+h),(0,0,255),2)
                #cv2.imshow('Dmark' + str(rc) + '.png',imtemp)
                cv2.imwrite('Dmark' + str(rc) + '.png',imtemp)
                
                        
                idx+=1
                print(str(idx) + " x = " + str(x) + " y = " + str(y) + " w = " + str(w) + " h = " + str(h))
                new_img=im[y:y+h,x:x+w]
                cv2.imwrite('Dval' + str(rc) + '.png',new_img)
                rc = rc + 1
                #cv2.imshow(str(idx) + '.png',new_img)
                gray3 = cv2.cvtColor(new_img,cv2.COLOR_BGR2GRAY)
                blur3 = cv2.GaussianBlur(gray3,(5,5),0)
                thresh3 = cv2.adaptiveThreshold(blur3,255,1,1,11,2)
                im3, contours3,hierarchy3 = cv2.findContours(thresh3,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                print(len(contours3))
                for c3 in contours3:
                    x3,y3,w3,h3 = cv2.boundingRect(c3)
                    if w3 > 10 and w3 < 100 and h3>20:

                        #print(str(w3))
                        new_img3=im3[y3:y3+h3,x3:x3+w3]
                        cv2.imwrite('temp.png',new_img3)
                        #cv2.imshow(str(idx) + str(w3) + '.png',new_img3)
                        basewidth = 10
                        img6 = Image.open('temp.png')
                        wpercent = (basewidth/float(img6.size[0]))
                        hsize = int((float(img6.size[1])*float(wpercent)))
                        img6 = img6.resize((50,50), Image.ANTIALIAS)
                        #img6.save('temp2.png') 

                        #img_file = Image.open('temp2.png')
                        img_file = img6
                        # img_file.show()

                        # get original image parameters...
                        width, height = img_file.size
                        format = img_file.format
                        mode = img_file.mode

                        # Make image Greyscale
                        img_grey = img_file.convert('L')
                        #img_grey.save('result.png')
                        #img_grey.show()

                        # Save Greyscale values
                        value = np.asarray(img_grey.getdata(), dtype=np.int).reshape((img_grey.size[1], img_grey.size[0]))
                        value = value.flatten()
                        #print(value)
                        with open("img_pixels.csv", 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow(value)
        



    y2=y
    #cv2.imwrite(str(idx) + " x = " + str(x) + " y = " + str(y) + " w = " + str(w) + " h = " + str(h) + '.png', new_img)


my_data = genfromtxt('img_pixels.csv', delimiter=',')    

print(len(my_data))
i =0
for myitem in my_data:
    i= i +1
    my_data7 = myitem.reshape((50,50))
    #print(my_data7)
    #cv2.imshow(str(i) + '.png',my_data7)

clf = svm.SVC(gamma=0.001)
traindata = np.arange(48)
clf.fit(my_data,traindata)

prediction = clf.predict(my_data[1:2])
print("predicted digit -> ", prediction)


#cv2.imshow("im",im)


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

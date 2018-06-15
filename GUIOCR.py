from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import argparse
import imutils
import cv2
import sys
import os
import csv
from numpy import genfromtxt
from sklearn import datasets, svm, metrics
from subprocess import Popen
import shutil
from numpy import array
from tkinter import messagebox


master = Tk()
checkboxvar = IntVar()
textboxvar = StringVar()

canvas_width = 1000
canvas_height =1000

canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack()



#img = PhotoImage(file="Pic-d.png")

def callback():
    print("click!")
    img = Image.open("DInputPage1.png")
    pil_image2 = img.resize((600, 900), Image.ANTIALIAS)
    filename = ImageTk.PhotoImage(pil_image2)
    #canvas = Canvas(master,height=600,width=900)
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(10,10,anchor='nw',image=filename)
    canvas.pack()

def browsebutton():
    for item in os.listdir():
        if item.startswith('D'):
            os.remove(item)
    file_path = filedialog.askopenfilename()
    print(file_path)
    shutil.copy(file_path,os.curdir)
    print(os.path.basename(file_path))
    os.rename(os.path.basename(file_path), "TempInput.pdf")
    p = Popen("GS.bat")
    stdout, stderr = p.communicate()
    imagedefault()
    readimage()

def imagedefault():
    img = Image.open("DInputPage1.png")
    pil_image2 = img.resize((600, 900), Image.ANTIALIAS)
    filename = ImageTk.PhotoImage(pil_image2)
    #canvas = Canvas(master,height=600,width=900)
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(10,60,anchor='nw',image=filename)
    canvas.pack()
    
    print("imageupload")


def imageupdate(img_name):
    img = Image.open(img_name)
    pil_image2 = img.resize((600, 900), Image.ANTIALIAS)
    filename = ImageTk.PhotoImage(pil_image2)
    #canvas = Canvas(master,height=600,width=900)
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(10,60,anchor='nw',image=filename)
    canvas.pack()
    
    print("imageupdated")

def charupdateupdate(img_name):
    img = Image.open(img_name)
    pil_image2 = img.resize((50, 50), Image.ANTIALIAS)
    filename = ImageTk.PhotoImage(pil_image2)
    #canvas = Canvas(master,height=600,width=900)
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(10,100,anchor='nw',image=filename)
    canvas.pack()
    
    print("imageupdated")
    
def checkupdate():
    print(checkboxvar.get())

def readimage():
    looprc2 = 10
    pagenumber = 0
    for item in os.listdir():
        if item.startswith('DInputPage'):
            pagenumber = pagenumber + 1
            imageupdate(item)
            im = cv2.imread(item)
            im3 = im.copy()
            imorg = im.copy()
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
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
                with open("MainSplit.csv", 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(str(x) + "," + str(y) + "," + str(w) + "," + str(h))
                                    
                if w>30 and h>40 and h<90 and (y2-y) > 3:
                    imtemp = imorg.copy()
                    cv2.rectangle(imtemp,(x,y),(x+w,y+h),(0,0,255),2)
                    cv2.imwrite('Dmark' + 'P' + str(pagenumber) + 'N' + str(rc) + '.png',imtemp)
                    idx+=1
                    print(str(idx) + " x = " + str(x) + " y = " + str(y) + " w = " + str(w) + " h = " + str(h))
                    new_img=im[y:y+h,x:x+w]
                    cv2.imwrite('Dval' + 'P' + str(pagenumber) + 'N' + str(rc) + '.png',new_img)
                    rc = rc + 1
                    gray3 = cv2.cvtColor(new_img,cv2.COLOR_BGR2GRAY)
                    blur3 = cv2.GaussianBlur(gray3,(5,5),0)
                    thresh3 = cv2.adaptiveThreshold(blur3,255,1,1,11,2)
                    im3, contours3,hierarchy3 = cv2.findContours(thresh3,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                    print(len(contours3))
                    for c3 in contours3:
                        x3,y3,w3,h3 = cv2.boundingRect(c3)
                        with open("SubSplit.csv", 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow(str(x) + "," + str(y) + "," + str(w) + "," + str(h))
                            
                        if w3 > 10 and w3 < 100 and h3>20:
                            new_img3=im3[y3:y3+h3,x3:x3+w3]
                            cv2.imwrite('temp.png',new_img3)
                            #cv2.imshow(str(idx) + str(w3) + '.png',new_img3)
                            basewidth = 10
                            img6 = Image.open('temp.png')
                            wpercent = (basewidth/float(img6.size[0]))
                            hsize = int((float(img6.size[1])*float(wpercent)))
                            img6 = img6.resize((50,50), Image.ANTIALIAS)
                            img_file = img6
                            width, height = img_file.size
                            format = img_file.format
                            mode = img_file.mode
                            img_grey = img_file.convert('L')
                            value = np.asarray(img_grey.getdata(), dtype=np.int).reshape((img_grey.size[1], img_grey.size[0]))
                            value = value.flatten()
                            flagfound = 0
                            
                            
                            with open("img_pixels.csv") as fh:
                                csv_reader = csv.reader (fh)
                                for row in csv_reader:
                                    print(row)
                                    if (array(row) == value):
                                        flagfound = 1    
                                    print(type(array(row)))
                                    print("=======")
                                    print(type(value))
                                    #file_1_tuples.append(  tuple(row)  )
                            if flagfound == 0 and checkboxvar.get() ==1:
                                with open("img_pixels.csv", 'a') as f:
                                    writer = csv.writer(f)
                                    writer.writerow(value)
                                
##                                textbox = Entry(master, text="ddfdfd", textvariable=lambda: textboxvar)
##                                #textbox.configure(width = 8, activebackground = "#33B5E5", relief = RAISED)
##                                textbox_window = canvas.create_window(750, looprc2, anchor=NW, window=textbox)
##                                
##                                filename = ImageTk.PhotoImage(img_file)
##                                #canvas = Canvas(master,height=600,width=900)
##                                canvas.image = filename  # <--- keep reference of your image
##                                canvas.create_image(850,looprc2,anchor=NW ,image=filename)
##                                #canvas.pack()
##                                
##                                looprc2 = looprc2 + 20
##                                
                                try:
                                    #charupdateupdate(img6)
                                    
                                    print("No error")
                                except:
                                    print("This is an error message!")
                                print(textboxvar.get())
                                
                                
                            #with open("img_pixels.csv", 'a') as f:
                            #    writer = csv.writer(f)
                            #    writer.writerow(value)
                y2=y
            
    
# ... snip ...
button1 = Button(master, text = "Quit", command = callback, anchor = W)
button1.configure(width = 10, activebackground = "#33B5E5", relief = RAISED)
button1_window = canvas.create_window(610, 60, anchor=NW, window=button1)

button2 = Button(master, text = "Browse", command = browsebutton, anchor = W)
button2.configure(width = 8, activebackground = "#33B5E5", relief = RAISED)
button2_window = canvas.create_window(610, 10, anchor=NW, window=button2)

checkbu = Checkbutton(master, text="Train", command = checkupdate, variable=checkboxvar)
checkbu.configure(width = 8, activebackground = "#33B5E5", relief = RAISED)
checkbu_window = canvas.create_window(700, 10, anchor=NW, window=checkbu)

textbox = Entry(master, text="ddfdfd", textvariable=textboxvar)
#textbox.configure(width = 8, activebackground = "#33B5E5", relief = RAISED)
textbox_window = canvas.create_window(750, 10, anchor=NW, window=textbox)




mainloop()

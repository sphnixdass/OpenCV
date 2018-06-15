from tempfile import NamedTemporaryFile
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
import fileinput

irc = 1


master = Tk()
checkboxvar = IntVar()
textboxvar = StringVar()

canvas_width = 280
canvas_height =80

canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack()
textbox = Entry(master, text="ddfdfd", textvariable=textboxvar)
textbox.configure(width = 3)
textbox_window = canvas.create_window(100, 10, anchor=NW, window=textbox)



def readcsv():
    deleteempytrow()
    my_data = genfromtxt('img_pixels.csv', delimiter=',')    
    print(len(my_data))
    i =0
    for myitem in my_data:
        i= i +1
        if int(myitem[2500]) == 1:
            
            irc = i
            print(str(len(myitem)) + "   " + str(irc) + "  " + str(myitem[2500]))
            myitem = myitem[0:2500]
            my_data7 = myitem.reshape((50,50))
            cv2.imwrite('DtempChar.png',my_data7)
            img = Image.open("DtempChar.png")
            #pil_image2 = img.resize((50, 50), Image.ANTIALIAS)
            filename = ImageTk.PhotoImage(img)
            #canvas = Canvas(master,height=600,width=900)
            canvas.image = filename  # <--- keep reference of your image
            canvas.create_image(10, 10,anchor='nw',image=filename)
            canvas.pack()
            return
        
def updatecsv():
    
    filename = 'img_pixels.csv'

    my_data = genfromtxt('img_pixels.csv', delimiter=',')    
    print(len(my_data))
    i =0
    for myitem in my_data:
        i= i +1
        if int(myitem[2500]) == 1:
            irc = i
            i = 0
            with open(filename,'r') as csvinput:
                with open('output.csv', 'w') as csvoutput:
                    writer = csv.writer(csvoutput)
                    for row in csv.reader(csvinput):
                        i= i +1
                        #print("len" + str(len(row)))
                        if (i == irc):
                            print("success" + str(irc) + "  " + str(len(row)))
                            row[2500] = ord(textboxvar.get())
                            writer.writerow(row)
                        else:
                            writer.writerow(row)
            shutil.move('output.csv', filename)
            return


def deletecsv():
    
    filename = 'img_pixels.csv'

    my_data = genfromtxt('img_pixels.csv', delimiter=',')    
    print(len(my_data))
    i =0
    for myitem in my_data:
        i= i +1
        if int(myitem[2500]) == 1:
            irc = i
            i = 0
            with open(filename,'r') as csvinput:
                with open('output.csv', 'w') as csvoutput:
                    writer = csv.writer(csvoutput)
                    for row in csv.reader(csvinput):
                        i= i +1
                        #print("len" + str(len(row)))
                        if (i == irc):
                            print("delete" + str(irc) + "  " + str(len(row)))
                            #row[2500] = ord(textboxvar.get())
                            #writer.writerow(row)
                        else:
                            writer.writerow(row)
            shutil.move('output.csv', filename)
            return

                
def updatetrigger():
    deleteempytrow()
    print("sss" + str(irc))
    updatecsv()
    readcsv()

def deleteempytrow():
    filename = 'img_pixels.csv'
    fh = open(filename, "r")
    lines = fh.readlines()
    fh.close()

    keep = []
    for line in lines:
        if len(line) > 2505:
            keep.append(line)

    fh = open(filename, "w")
    fh.write("".join(keep))
    # should also work instead of joining the list:
    # fh.writelines(keep)
    fh.close()

def updatedelete():
    deletecsv()
    readcsv()
    
readcsv()

button1 = Button(master, text = "Add", command = updatetrigger, anchor = W)
button1.configure(width = 5, activebackground = "#33B5E5", relief = RAISED)
button1_window = canvas.create_window(150, 10, anchor=NW, window=button1)

button1 = Button(master, text = "Delete", command = deletecsv, anchor = W)
button1.configure(width = 8, activebackground = "#33B5E5", relief = RAISED)
button1_window = canvas.create_window(200, 10, anchor=NW, window=button1)

      
##for x in range(2, 4):
##    print(x)
##    img = Image.open("DtempChar" + str(x) + ".png")
##    #pil_image2 = img.resize((50, 50), Image.ANTIALIAS)
##    filename = ImageTk.PhotoImage(img)
##    #canvas = Canvas(master,height=600,width=900)
##    canvas.image = filename  # <--- keep reference of your image
##    canvas.create_image(10, x*20,anchor='nw',image=filename)
##    canvas.pack()

        
mainloop()

    #print(my_data7)
    #cv2.imshow(str(i) + '.png',my_data7)

##clf = svm.SVC(gamma=0.001)
##traindata = np.arange(len(my_data))
##clf.fit(my_data,traindata)
##
##prediction = clf.predict(my_data[1:2])
##print("predicted digit -> ", prediction)



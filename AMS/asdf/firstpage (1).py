#import module from tkinter for UI

from tkinter import *
import os
from datetime import datetime;

#creating instance of TK
root=Tk()
root.configure(background="white")

#root.geometry("300x300")

def function1():
    os.system("py dataset_capture.py")
def function2():
    os.system("py training_dataset.py")
def function3():
    os.system("py recognizer.py")
def function4():
    root.destroy()

root.title("AUTOMATIC ATTENDANCE MANAGEMENT USING FACE RECOGNITION")
#creating a text label
Label(root, text="FACE RECOGNITION ATTENDANCE SYSTEM",font=("times new roman",20),fg="white",bg="purple",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
#creating first button
Button(root,text="Create Dataset",font=("times new roman",20),bg="black",fg='white',command=function1).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
#creating second button
Button(root,text="Train Dataset",font=("times new roman",20),bg="black",fg='white',command=function2).grid(row=4,columnspan=2,sticky=W+E,padx=5,pady=5)
#creating third button
Button(root,text="Recognize",font=('times new roman',20),bg="black",fg="white",command=function3).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
Button(root,text="Exit",font=('times new roman',20),bg="maroon",fg="white",command=function4).grid(row=9,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
root.mainloop()
import tkinter as tk
from tkinter import E, W, N, S
from PIL import ImageTk
from PIL import Image
import numpy as np


def showpoints(oldpoints,newpoints,pradii,File):
    """Show the image again along with the uncertainty circles,
    plotting the optimized points on top.

    Inputs =>
      oldpoints: old points guessed by user
      newpoints: optimized joint image points
      pradii: uncertainty radii
      File: filename of image
    """
    root = tk.Tk()
    
    #setting up a tkinter canvas with scrollbars
    frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = tk.Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = tk.Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=tk.BOTH,expand=1)
    
    #adding the image
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(width=img.width(), height=img.height(), scrollregion=canvas.bbox(tk.ALL))
   
    oldpoints = np.copy(oldpoints)
    newpoints = np.copy(newpoints)
    oldpoints[:,1] = img.height()-oldpoints[:,1]
    newpoints[:,1] = img.height()-newpoints[:,1]
    linewidthouter=3
    linewidthinner=1
    for i in range(len(pradii)):
        circle = canvas.create_oval(oldpoints[i,0]-pradii[i],oldpoints[i,1]-pradii[i],oldpoints[i,0]+pradii[i],oldpoints[i,1]+pradii[i],stipple="gray12",fill="green")
        canvas.create_line(oldpoints[i,0]-5,oldpoints[i,1]-5,oldpoints[i,0]+5,oldpoints[i,1]+5,width=linewidthouter)
        canvas.create_line(oldpoints[i,0]-5,oldpoints[i,1]+5,oldpoints[i,0]+5,oldpoints[i,1]-5,width=linewidthouter)
        canvas.create_line(oldpoints[i,0]-5,oldpoints[i,1]-5,oldpoints[i,0]+5,oldpoints[i,1]+5,width=linewidthinner,fill="white")
        canvas.create_line(oldpoints[i,0]-5,oldpoints[i,1]+5,oldpoints[i,0]+5,oldpoints[i,1]-5,width=linewidthinner,fill="white")
    for i in range(len(pradii)):
        canvas.create_line(newpoints[i,0]-5,newpoints[i,1]-5,newpoints[i,0]+5,newpoints[i,1]+5,width=linewidthouter, fill="red")
        canvas.create_line(newpoints[i,0]-5,newpoints[i,1]+5,newpoints[i,0]+5,newpoints[i,1]-5,width=linewidthouter, fill="red")
        canvas.create_line(newpoints[i,0]-5,newpoints[i,1]-5,newpoints[i,0]+5,newpoints[i,1]+5,width=linewidthinner,fill="yellow")
        canvas.create_line(newpoints[i,0]-5,newpoints[i,1]+5,newpoints[i,0]+5,newpoints[i,1]-5,width=linewidthinner,fill="yellow")


    root.mainloop()
    

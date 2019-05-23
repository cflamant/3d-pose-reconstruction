import tkinter as tk
from tkinter import E, W, N, S
from tkinter import filedialog
from PIL import ImageTk
from PIL import Image
import numpy as np


def selectpoints():
    """Brings up tkinter gui for selecting an image, and then prompts
    the user to enter joint locations in order. There are also buttons
    on the right that are used for setting up the relative order array.

    Returns =>
      points: 2D image points of joint locations
      pradii: Radius of uncertainty in the joint locations
      relorder: augmented relative order array
      File: filename of opened image
    """
    root = tk.Tk()
    ijoint = 0
    jointcount = 12
    points = np.zeros((12,2))
    pradii = np.zeros(12)
    relorder = np.zeros(11)
    jointnames = ["right shoulder", "left shoulder", "right hip", "left hip", "right elbow", "left elbow", "right knee", "left knee", "right wrist", "left wrist", "right ankle", "left ankle"]
    
    buttonnames=[["Right Shoulder","Left Shoulder"],["Base of Neck","Tailbone"],["Right Hip","Left Hip"],["Right Elbow","Right Shoulder"],["Left Elbow", "Left Shoulder"],["Right Knee","Right Hip"],["Left Knee","Left Hip"],["Right Wrist","Right Elbow"],["Left Wrist","Left Elbow"],["Right Ankle","Right Knee"],["Left Ankle","Left Knee"]]
    
    buttonvars = []
    for i in range(11):
        buttonvars.append(tk.IntVar())
    
    buttons = []

    isDown = False
    circle = None
    
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
    File = filedialog.askopenfilename(parent=root, initialdir="../images",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(width=img.width(), height=img.height(), scrollregion=canvas.bbox(tk.ALL))
    selectiontext = tk.Label(frame, text="")
    selectiontext.grid(row=0,column=0, sticky=N+W)
    
    buttonframe = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
    buttonframe.grid(row=0, column=2, sticky=N)
    instructions = tk.Label(buttonframe, text="From the following pairs, select\nwhich is closer to the camera.\nIf you're not 100% sure, skip.")
    instructions.grid(row=0,columnspan=2)
    
    for i in range(len(buttonnames)):
        choice = []
        for j in range(len(buttonnames[0])):
            # value is +1 if first choice is selected, -1 if second
            choice.append(tk.Radiobutton(buttonframe, indicatoron=0,
                                         text=buttonnames[i][j], pady=8,
                                         variable=buttonvars[i],width=15,
                                         value=1-2*j))
        buttons.append(choice)
    
    for i in range(len(buttons)):
        for j in range(len(buttons[0])):
            buttons[i][j].grid(row=i+1, column=j,pady=5)
    
    
    # Set the text informing which joint should be selected
    def updateselectiontext():
        if(ijoint >= jointcount):
            newtext = "Specify joint ordering then click the next button"
        else:
            newtext = "Click (and drag) on the " + jointnames[ijoint]
        selectiontext.config(text=newtext)
    
    updateselectiontext()
    
    #Return the points and relative order
    def nextaction():
        nonlocal relorder
        for i in range(len(buttonvars)):
            relorder[i] = buttonvars[i].get()
        root.destroy()

    nextbutton = tk.Button(buttonframe, text="Next", state='disabled',command=nextaction)
    nextbutton.grid(row=len(buttonnames)+1,column=1,pady=14)

    #undo one joint selection
    def undo():
        nonlocal ijoint
        if ijoint > 0:
            ijoint -= 1
            canvas.delete("mark"+str(ijoint))
            updateselectiontext()
            nextbutton.config(state='disabled')
        
    
    # undo button
    undobutton = tk.Button(buttonframe, text="Undo", command=undo)
    undobutton.grid(row=len(buttonnames)+1,column=0,pady=14)

    #Reset joints
    def resetjoints():
        nonlocal ijoint
        ijoint = 0
        canvas.delete("marker")
        updateselectiontext()
        nextbutton.config(state='disabled')
        
    
    # Reset button
    resetbutton = tk.Button(buttonframe, text="Reset", command=resetjoints)
    resetbutton.grid(row=len(buttonnames)+2,column=0,pady=0)


    
    #function to be called when mouse is clicked
    def getcoords(event):
        nonlocal ijoint, points, isDown, circle
        if ijoint < jointcount:
            linewidthouter=3
            linewidthinner=1
            # Start uncertainty circle
            circle = canvas.create_oval(event.x-1,event.y-1,event.x+1,event.y+1,tags=("marker","mark"+str(ijoint)),stipple="gray12",fill="green")
            canvas.create_line(event.x-5,event.y-5,event.x+5,event.y+5,width=linewidthouter,tags=("marker","mark"+str(ijoint)))
            canvas.create_line(event.x-5,event.y+5,event.x+5,event.y-5,width=linewidthouter,tags=("marker","mark"+str(ijoint)))
            canvas.create_line(event.x-5,event.y-5,event.x+5,event.y+5,width=linewidthinner,fill="white",tags=("marker","mark"+str(ijoint)))
            canvas.create_line(event.x-5,event.y+5,event.x+5,event.y-5,width=linewidthinner,fill="white",tags=("marker","mark"+str(ijoint)))
            #saving x and y coords to points array
            points[ijoint,0] = float(event.x)
            points[ijoint,1] = img.height()-float(event.y)
        isDown = True
    #function to be called when mouse is released
    def release(event):
        nonlocal isDown, ijoint, pradii
        if ijoint < jointcount:
            coordinates=canvas.coords(circle)
            radius = np.abs(coordinates[2]-coordinates[0])/2.
            pradii[ijoint] = radius
            ijoint += 1
        isDown = False
        if ijoint >= jointcount:
            nextbutton.config(state='normal')
        updateselectiontext()
        
    # Only activate when mouse is held down.
    def motion(event):
        nonlocal circle
        if isDown:
            coordinates=canvas.coords(circle)
            centerx = (coordinates[0]+coordinates[2])//2
            centery = (coordinates[1]+coordinates[3])//2
            radius = int(np.sqrt( (event.x-centerx)**2+(event.y-centery)**2))
            canvas.coords(circle,centerx-radius,centery-radius,centerx+radius,centery+radius)
        
    #mouseclick event
    canvas.bind("<Button 1>",getcoords)
    canvas.bind("<ButtonRelease 1>",release)
    canvas.bind("<Motion>",motion)


    root.mainloop()
    return points, pradii, relorder, File
    

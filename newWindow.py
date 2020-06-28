from tkinter import * 
from tkinter.ttk import *
  
  
class NewWindow(Toplevel): 
      
    def __init__(self, master = None): 
          
        super().__init__(master = master) 
        self.geometry("200x200") 
        self.title("Enhorabuena!!") 
        frame2 = PhotoImage(file="Resources/firework.gif", format="gif -index 2")
        label = Label(self,  image=frame2) 
        label.pack() 
  
  
## creates a Tk() object 
#master = Tk() 
  
## sets the geometry of  
## main root window 
#master.geometry("200x200") 
  
#label = Label(master, text ="This is the main window") 
#label.pack(side = TOP, pady = 10) 
  
## a button widget which will 
## open a new window on button click 
#btn = Button(master,  
#             text ="Click to open a new window") 
  
## Following line will bind click event 
## On any click left / right button 
## of mouse a new window will be opened 
#btn.bind("<Button>",  
#         lambda e: NewWindow(master)) 
  
#btn.pack(pady = 10) 
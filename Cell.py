from tkinter import *
from PIL import ImageTk, Image

class Cell(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._color = 'white'
        #self.colorD = "pink"
        self._text = StringVar()
        self._image=ImageTk.PhotoImage(Image.open("Resources/background1.png"))
        self.is_explosive = False
        self.mine_counter = 0
        self.is_flagged = 0
        self.swept = False
        self.configure(
             image=self._image
             ,bg=self._color
            ,relief=GROOVE
            ,borderwidth=3
            ,width=1
            ,height=1 
            #,disabledforeground=self.colorD
        )
        
    def show_text(self):
        self.config(textvar=self._text)
    
    def hide_text(self):
        self.configure(textvar=None)
        
    def disable(self):
        self.config(state=DISABLED)
        self.unbind('<Button-1>')
        self.unbind('<Button-3>')
       
    @property
    def image(self):
        return self._image
        
    @image.setter
    def image(self, c):
        self._image = c
        self.config(image=self._image)
        
    @property
    def color(self):
        return self._color
        
    @color.setter
    def color(self, c):
        self._color = c
        self.config(bg=self._color)
      
    #@property
    #def colorD(self):
    #    return self._colorD
        
    #@colorD.setter
    #def colorD(self, c):
    #    self._colorD = c
    #    self.config(disabledforeground=self._colorD)
        
    @property
    def text(self):
        return self._text.get()
    
    @text.setter
    def text(self, t):
        self._text.set(str(t))

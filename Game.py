from Aplication import *
from tkinter import *
from tkinter import font
#------------------------------------------------------
#Inicio Aplicacion
#------------------------------------------------------

def inicio():
    global bcolor
    app = App()
    app['background']=bcolor
    app.Draw()
    app.Refresher()
    app.mainloop()

#------------------------------------------------------
inicio()
#------------------------------------------------------
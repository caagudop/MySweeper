from tkinter import *
from tkinter import messagebox
from Cell import Cell
from PIL import ImageTk, Image
import random
import os
import time

#------------------------------------------------------
# Metodo poblacion bombas 
#------------------------------------------------------

def getRandomSeed(num):
    lista=[]
    while len(lista)<=num:
        rand = random.randint(0,77)
        if rand not in lista:
            lista.append(rand)
    return lista

bcolor="#c9c9c9"
tcolor="#000000"


class App(Tk):
   
  #------------------------------------------------------
  # Constructor
  #------------------------------------------------------
    
    def __init__(self, *args, **kwargs):
        try:
            self.grid_dimentions = kwargs.pop('dimentions')
        except KeyError:
            self.grid_dimentions = 8
        super().__init__(*args, **kwargs)
        self.title('BuscaMinas')
        self.geometry('{0}x{0}'.format(self.grid_dimentions*50))
        self.dificultad = 1
        self.numBoombs=5
        self.resizable(False, False)
        self.plantedBoombs =getRandomSeed(5)
        dicrWin={
         "muy facil":[],
         "facil":[],
         "medio":[],
         "dificil":[],
         "extreme":[]
         }  
        self.dicrW=dicrWin
        self.inicio=0
        self.tiempo=0
        self.crono=True
        global bcolor
        global tbcolor
        self.dificL=Label(self,text='', bg=bcolor, fg=tcolor)
        self.dificL.pack(side=TOP, fill=X) 
        self.frameCreate()
        self.footer = Button(self, text="Reset",command=self.reset, bd=3, relief=RIDGE, bg='#6DB6FF')
        self.footer.pack(after=self.bomb_area, side=BOTTOM) 
  

    def updateDictW(self, time=0, bmos=False):
        if bmos:
         dificD=["muy facil","facil","medio","dificil","extreme"]       
         ari=self.dicrW[dificD[self.dificultad]]
         ari.append(time)
         ari.sort(reverse=False)
         self.dicrW[dificD[self.dificultad]]=ari
        else:
         pass

    
  #------------------------------------------------------      
  #StartMethods
  #------------------------------------------------------
    
    def menuCreate(self):
        global dific
        menubar = Menu(self)
        self.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Muy Facil", command=self.veasy)
        filemenu.add_command(label="Facil", command=self.easy)
        filemenu.add_command(label="Medio", command=self.medium)
        filemenu.add_command(label="Dificil", command=self.hard)
        filemenu.add_command(label="Extremo", command=self.extreme)
        menubar.add_cascade(label="Dificultad", menu=filemenu)
        menubar.add_cascade(label="LeaderBoard", command=self.nwindowB)
        dificD=["Muy Facil","Facil","Medio","Dificil","Extremo"]       
        self.dificL.configure(text="Dificultad: " + dificD[self.dificultad])

  #------------------------------------------------------
      
    def frameCreate(self, dificultad=1):
        self.menuCreate()    
        self.inicio=time.time()
        self.tiempo=0
        self.crono=True
        self.bomb_area = Frame(self)
        self.cells = []
        self.cells_discovered = 0
        self.mines_flagged = 0
        cont = 0

        for row in range(self.grid_dimentions):
            self.cells.append(list())
            Grid.rowconfigure(self.bomb_area, row, weight=1)
            for column in range(self.grid_dimentions):
                cont = cont +1
                Grid.columnconfigure(self.bomb_area, column, weight=1)
                cell = self.make_cell(column, row)
                cell.grid(row=row, column=column, sticky='NEWS')
                self.cells[-1].append(cell)

    # configure squares adjacent to mines with adjacent mine count
        for r in range(self.grid_dimentions):
            for c in range(self.grid_dimentions):
                if self.cells[r][c].is_explosive:
                    for cell in self.adjacentCells(self.cells[r][c]):
                        cell.mine_counter += 1

        self.bomb_area.pack(expand=True, fill=BOTH)

  #------------------------------------------------------

    def adjacentCells(self, cell):
        # get all cells in cell grid, ignoring all edge cases pun intended
        r,c = self.locate_cell(cell)
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if i < 0 or j < 0:
                    continue  # avoid rotational indexes
                if i == r and j == c:
                    continue  # skip the cell itself
                try:
                    yield self.cells[i][j]
                except IndexError:
                    pass

  #------------------------------------------------------      
  # Difficulty
  #------------------------------------------------------

    def veasy(self):
        self.dificultad=0
        self.numBoombs=2
        self.plantedBoombs = getRandomSeed(1)
        self.reset()
    def easy(self):
        self.dificultad=1
        self.numBoombs=5
        self.plantedBoombs = getRandomSeed(5)
        self.reset()
    def medium(self):
        self.dificultad=2
        self.numBoombs=10
        self.plantedBoombs = getRandomSeed(10)
        self.reset()
    def hard(self):
        self.dificultad=3
        self.numBoombs=25
        self.plantedBoombs = getRandomSeed(25)
        self.reset()
    def extreme(self):
        self.dificultad=4
        self.numBoombs=50
        self.plantedBoombs = getRandomSeed(50)
        self.reset()

  #------------------------------------------------------
  # LogicMethods
  #------------------------------------------------------

    def locate_cell(self, cell):
        for r in range(self.grid_dimentions):
            for c in range(self.grid_dimentions):
                if self.cells[r][c] is cell:
                    return r,c

  #------------------------------------------------------

    def sweep(self, cell):
        if cell.swept:
            return
        if cell.is_flagged:
            return
        cell.swept = True
        if cell.mine_counter > 0:
            auxk = cell.mine_counter
            if auxk>0 or auxk is not None:
                try:
                    rutad = "Resources/count"+str(auxk)+".png"
                    imgt=Image.open(rutad)
                except:
                    rutad = "Resources/count.png"
                    imgt=Image.open(rutad)
            imgt = imgt.resize((40, 40), Image.ANTIALIAS)
            cell.image=ImageTk.PhotoImage(imgt)
            cell.show_text()
        else:
            try:
                rutad = "Resources/count"+str(auxk)+".png"
                imgt=Image.open(rutad)
            except:
                rutad = "Resources/count.png"
                imgt=Image.open(rutad)
            imgt = imgt.resize((40, 40), Image.ANTIALIAS)
            cell.image=ImageTk.PhotoImage(imgt)
            # recursively reveal empty cells
            for adj_cell in self.adjacentCells(cell):
                self.sweep(adj_cell)
        cell.color = 'white'
        cell.unbind('<Button-1>')
        cell.unbind('<Button-3>')
        self.cells_discovered += 1
        self.check_victory()

  #------------------------------------------------------

    def explode_mine(self, mine):
        if  mine.is_flagged:
            return
        for row in self.cells:
            for cell in row:
                if cell.is_explosive:
                    imgt=Image.open("Resources/bomb.png")
                    imgt = imgt.resize((40, 40), Image.ANTIALIAS)
                    cell.image=ImageTk.PhotoImage(imgt)
                    cell.color = 'red'
        self.nwindow(False)    
 

  #------------------------------------------------------

    def toggle_flag(self, cell):
        cell.is_flagged ^= 1
        if cell.is_flagged:
            cell.text=''
            cell.color = 'blue'
            imgt=Image.open("Resources/minesweeperflag.png")
            imgt = imgt.resize((40, 40), Image.ANTIALIAS)
            cell.image = ImageTk.PhotoImage(imgt)
            cell.show_text()
            if cell.is_explosive:
                self.mines_flagged += 1
        else:
            if cell.color == 'blue':
                cell.text=''
                auxk = cell.mine_counter 
                rutad = "Resources/background1.png"
                imgt=Image.open(rutad)
                cell.image=ImageTk.PhotoImage(imgt)
                cell.color = 'white'
                cell.hide_text()
                if cell.is_explosive:
                    self.mines_flagged -= 1
        self.check_victory()

  #------------------------------------------------------

    def make_cell(self, x, y):
        c = Cell(self.bomb_area)
        num = x*10+y
        # TODO: implement a better algorithm for distributing mines
        if num in self.plantedBoombs:
            c.is_explosive = True
        if c.is_explosive:
            c.bind('<Button-1>', lambda cb: self.explode_mine(c))
        else:
            c.bind('<Button-1>', lambda cb: self.sweep(c))
        c.bind('<Button-3>', lambda cb: self.toggle_flag(c))
        return c
        
  #------------------------------------------------------
  # EndMethodss
  #------------------------------------------------------
    def reset(self, d=1):
        for widget in self.bomb_area.winfo_children():
            widget.destroy()
        self.bomb_area.pack_forget()
        self.plantedBoombs =getRandomSeed(self.numBoombs)
        self.frameCreate(dificultad=d)
          
    def check_victory(self):
        if self.mines_flagged + self.cells_discovered == self.grid_dimentions**2:
            self.crono=False
            self.nwindow(True)
            
  #------------------------------------------------------      
  # WinLoose
  #------------------------------------------------------
    def nwindow(self, bwin=False):
        self.grab_set()
        nwin = Toplevel()
        nwin.grab_set()
        nwin.geometry('250x200')
        nwin.protocol("WM_DELETE_WINDOW", lambda: (nwin.destroy(), self.grab_release(), self.reset()))
        nwin.resizable(False, False)
        end= self.tiempo
        timer=self.inicio
        varT= end-timer
        if varT < 0:
            varT=0
        minutes, seconds = divmod(varT, 60)
        seconds = str(int(seconds)).zfill(2)
        tt = "Tiempo: "+"{:0>2}:{}".format(int(minutes),seconds)
        tile="Oh vaya!!!!"
        ruta="Resources/decepcion.png"
        texto="¡Has perdido!"
        if bwin:
            tile="Enhorabuena!!!!"
            ruta="Resources/firecracker.png"
            texto="¡Has ganado!"
        nwin.title(tile)
        imgt=Image.open(ruta)
        imgt = imgt.resize((100, 100), Image.ANTIALIAS)
        photo2= ImageTk.PhotoImage(imgt)
        lbl2 = Label(nwin, image = photo2)
        lbl2.pack()
        aa = Label(nwin,text =texto,width=1000, font = "Courier 20")
        aa.pack()
        ab = Label(nwin,text =tt,width=1000, font = "Courier 14")
        ab.pack()
        b= Button(nwin,text="OK",command= lambda : (nwin.destroy(), nwin.grab_release(), self.reset(), self.updateDictW(bmos=bwin, time=end-timer) ), bd=3, relief=RIDGE, bg='#6DB6FF')
        b.pack() 
        nwin.mainloop()  
        
  #------------------------------------------------------      
  # ScoreBoard
  #------------------------------------------------------
    def nwindowB(self, binlcuir=False, time=0):
        global dicrWin
        dificD=["muy facil","facil","medio","dificil","extreme"]
        #if binlcuir:
        #    self.updateDictW(time=time)
        ari=self.dicrW[dificD[self.dificultad]]
        nwin = Toplevel()
        nwin.grab_set()
        nwin.geometry('500x450')
        nwin.resizable(False, False)
        tile="Tabla de ganadores"
        ruta="Resources/leader.png"
        nwin.title(tile)
        imgt=Image.open(ruta)
        imgt = imgt.resize((400, 140), Image.ANTIALIAS)
        photo2= ImageTk.PhotoImage(imgt)
        lbl2 = Label(nwin, image = photo2)
        lbl2.pack()
        lbl = Label(nwin, text="Dificultad: "+ str(dificD[self.dificultad]).capitalize(), font="Courier 20")
        lbl.pack()
        if len(ari)>0:
            for i in range(1, len(ari)+1):
                 value=ari[i-1]
                 minutes, seconds = divmod(value, 60)
                 seconds = str(int(seconds)).zfill(2)
                 vav=str(i) + ". Tiempo:  "+"{:0>2}:{}".format(int(minutes),seconds)
                 lbl = Label(nwin, text=vav, font="Courier 14")
                 lbl.pack()
        else:
            lbl = Label(nwin, text="Not Records yet", font="Courier 18", fg="red")
            lbl.pack()
        nwin.mainloop()
  

  #------------------------------------------------------
  # Timer
  #------------------------------------------------------
    
    def Refresher(self):
        if self.crono:
            global text
            timer=self.inicio
            end = time.time()
            self.tiempo= end
            minutes, seconds = divmod(end-timer, 60)
            seconds = str(int(seconds)).zfill(2)
            tt = "Tiempo: "+"{:0>2}:{}".format(int(minutes),seconds)
            text.configure(text=tt)
        self.after(1000, self.Refresher) # every second...

    def Draw(self):
        global text
        global bcolor
        global tcolor
        text=Label(self,text='Tiempo', bg=bcolor, fg=tcolor)
        text.pack(after=self.bomb_area, side=BOTTOM, fill=X) 

   #------------------------------------------------------

    
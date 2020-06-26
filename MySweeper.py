from tkinter import *
from tkinter import messagebox
import random
import os
import time


class Cell(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._color = 'blue'
        self._text = StringVar()
        self.is_explosive = False
        self.mine_counter = 0
        self.is_flagged = 0
        self.swept = False
        self.configure(
             bg=self._color
            ,relief=GROOVE
            ,borderwidth=3
            ,width=1
            ,height=1
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
    def color(self):
        return self._color
        
    @color.setter
    def color(self, c):
        self._color = c
        self.config(bg=self._color)
        
    @property
    def text(self):
        return self._text.get()
    
    @text.setter
    def text(self, t):
        self._text.set(str(t))
    
def getRandomSeed(num):
    lista=[]
    while len(lista)<=num:
        rand = random.randint(0,77)
        if rand not in lista:
            lista.append(rand)
    return lista

class App(Tk):
    
    def __init__(self, *args, **kwargs):
        try:
            self.grid_dimentions = kwargs.pop('dimentions')
        except KeyError:
            self.grid_dimentions = 8
        super().__init__(*args, **kwargs)
        self.title('BuscaMinas')
        self.geometry('{0}x{0}'.format(self.grid_dimentions*35))
        self.dificultad = 1
        self.numBoombs=5
        self.plantedBoombs =getRandomSeed(5)
        self.crearFrame()
        self.footer = Button(self, text="Reset",command=self.reset)
        self.footer.pack(after=self.bomb_area, side=BOTTOM)  

    def  Draw(self):
        global text
        text=Label(self,text='Tiempo')
        text.pack(after=self.bomb_area, side=BOTTOM) 

    def crearMenu(self):
        global dific
        menubar = Menu(self)
        self.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Muy Facil", command=self.mfacil)
        filemenu.add_command(label="Facil", command=self.facil)
        filemenu.add_command(label="Medio", command=self.medio)
        filemenu.add_command(label="Dificil", command=self.dificil)
        filemenu.add_command(label="Extremo", command=self.extreme)
        menubar.add_cascade(label="Dificultad", menu=filemenu)
        dific=Label(self,text='')
        dific.pack() 
        
  
    def mfacil(self):
        self.dificultad=0
        self.numBoombs=1
        self.plantedBoombs = getRandomSeed(1)
        self.reset()
    def facil(self):
        self.dificultad=1
        self.numBoombs=5
        self.plantedBoombs = getRandomSeed(5)
        self.reset()
    def medio(self):
        self.dificultad=2
        self.numBoombs=10
        self.plantedBoombs = getRandomSeed(10)
        self.reset()
    def dificil(self):
        self.dificultad=3
        self.numBoombs=25
        self.plantedBoombs = getRandomSeed(25)
        self.reset()
    def extreme(self):
        self.dificultad=4
        self.numBoombs=50
        self.plantedBoombs = getRandomSeed(50)
        self.reset()
           
   
    def crearFrame(self, dificultad=1):
        self.crearMenu()   
        global timer
        global dific
        dificD=["Muy Facil","Facil","Medio","Dificil","Extremo"]
        dific.configure(text="Dificultad: " + dificD[self.dificultad])
        timer = time.time()
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
        print(str(cont) + "---")
        #self.rellenarBombas()
    # configure squares adjacent to mines with adjacent mine count
        for r in range(self.grid_dimentions):
            for c in range(self.grid_dimentions):
                if self.cells[r][c].is_explosive:
                    for cell in self.get_adjacent_cells(self.cells[r][c]):
                        cell.mine_counter += 1

        self.bomb_area.pack(expand=True, fill=BOTH)

   
  
    def get_adjacent_cells(self, cell):
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
    
    
    def locate_cell(self, cell):
        for r in range(self.grid_dimentions):
            for c in range(self.grid_dimentions):
                if self.cells[r][c] is cell:
                    return r,c
   
    def sweep(self, cell):
        if cell.swept:
            return
        cell.swept = True
        if cell.mine_counter > 0:
            cell.text = cell.mine_counter
            cell.show_text()
        else:
            # recursively reveal empty cells
            for adj_cell in self.get_adjacent_cells(cell):
                self.sweep(adj_cell)
        cell.color = 'white'
        cell.disable()
        self.cells_discovered += 1
        self.check_victory()
        
    
    def explode_mine(self, mine):
        for row in self.cells:
            for cell in row:
                if cell.is_explosive and not cell.is_flagged:
                    cell.color = 'red'
        resul = messagebox.askquestion('Has perdido', '¿Volver a intentarlo?.')
        if resul == "yes":
            self.reset()
        elif resul == "no":
            self.salir()

    def reset(self, d=1):
        for widget in self.bomb_area.winfo_children():
            widget.destroy()
        self.bomb_area.pack_forget()
        self.plantedBoombs =getRandomSeed(self.numBoombs)
        self.crearFrame(dificultad=d)

    def salir(self):
        resul = messagebox.askquestion('Por favor juega conmigo','¿Estas seguro?')
        if resul == "yes":
            self.quit()
            self.destroy()
        elif resul == "no":
            self.reset()
          
    def toggle_flag(self, cell):
        cell.is_flagged ^= 1
        if cell.is_flagged:
            cell.text='♥'
            cell.color = 'green'
            cell.show_text()
            if cell.is_explosive:
                self.mines_flagged += 1
        else:
            if cell.color == 'green':
                cell.text=''
                cell.color = 'blue'
                cell.hide_text()
                self.mines_flagged -= 1
        self.check_victory()
    
    #def rellenarBombas(self):
    #    lista=[]
    #    for i in range(self.numBoombs):
    #        rand = random.randint(0,64)
    #        if rand not in lista:
    #            lista.append(rand)
    #        else:
    #            rand = random.randint(0,64)
    #            if rand not in lista:
    #                lista.append(rand)

    #    cont=0
    #    for r in range(self.grid_dimentions):
    #        for c in range(self.grid_dimentions):
    #            cell = self.cells[r][c]
    #            if cell.coordinates in lista:
    #                cell.is_explosive = True
    #                cell.bind('<Button-1>', lambda cb: self.explode_mine(cell))
    #                cont=cont+1
    #            else:
    #                cell.bind('<Button-1>', lambda cb: self.sweep(cell))
    #            cell.bind('<Button-3>', lambda cb: self.toggle_flag(cell))
    #            cont=cont+1

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
        


    def check_victory(self):
        print (self.mines_flagged, self.cells_discovered)
        if self.mines_flagged + self.cells_discovered == self.grid_dimentions**2:
            messagebox.showinfo('YOU WIN!!', "you didn't explode this time!!")

    
    def Refresher(self):
        global text
        global timer
        end = time.time()
        minutes, seconds = divmod(end-timer, 60)
        seconds = str(int(seconds)).zfill(2)
        tt = "Tiempo: "+"{:0>2}:{}".format(int(minutes),seconds)
        text.configure(text=tt)
        self.after(1000, self.Refresher) # every second...


def inicio():
    app = App()
    app.Draw()
    app.Refresher()
    app.mainloop()


inicio()
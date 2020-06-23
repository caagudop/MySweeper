from tkinter import *
from tkinter import messagebox
import random
import os



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
    
    


class App(Tk):
    def __init__(self, *args, **kwargs):

        try:
            self.grid_dimentions = kwargs.pop('dimentions')
        except KeyError:
            self.grid_dimentions = 8
        
        super().__init__(*args, **kwargs)
        self.title('BuscaMinas')
        self.geometry('{0}x{0}'.format(self.grid_dimentions*35))
   
         # initialize menu
        def crearMenu(self):
            menubar = Menu(self)
            self.config(menu=menubar)
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="Dificultad")
            filemenu.add_command(label="Abrir")
            filemenu.add_command(label="Guardar")
            filemenu.add_command(label="Cerrar")
            filemenu.add_separator()
            filemenu.add_command(label="Salir", command=self.quit)
            menubar.add_cascade(label="Archivo", menu=filemenu)
            
        # initialize cell grid
        def crearFrame(self):
            self.bomb_area=None
            self.bomb_area = Frame(self)
            self.cells = []
            self.cells_discovered = 0
            self.mines_flagged = 0
            for row in range(self.grid_dimentions):
                self.cells.append(list())
                Grid.rowconfigure(self.bomb_area, row, weight=1)
                for column in range(self.grid_dimentions):
                    Grid.columnconfigure(self.bomb_area, column, weight=1)
                    cell = self.make_cell()
                    cell.grid(row=row, column=column, sticky='NEWS')
                    self.cells[-1].append(cell)
        
        # configure squares adjacent to mines with adjacent mine count
            for r in range(self.grid_dimentions):
                for c in range(self.grid_dimentions):
                    if self.cells[r][c].is_explosive:
                        for cell in self.get_adjacent_cells(self.cells[r][c]):
                            cell.mine_counter += 1
            self.bomb_area.pack(expand=True, fill=BOTH)

        crearMenu(self)
        crearFrame(self)
  
        
    
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
        if resul == "si":
            reset()

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
    
    
    def make_cell(self):
        c = Cell(self.bomb_area)
        
        # TODO: implement a better algorithm for distributing mines
        if random.randint(0,4) == 0:
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

    def reset():
        


def inicio():
    app = App()
    app.mainloop()


inicio()
import random
from genevo.bitint import BitInt
from genevo.cell   import Cell, CellDeath, CellBirth

class TwoSidedGrid:

    def __init__ (self, xmax, ymax):

        self.__new = [
                [None for _ in range (ymax)]
                      for _ in range (xmax)
        ]

        self.flip ()

    def flip (self):

        self.__grid = self.__new
        self.__new  = [l.copy () for l in self.__grid]

    def __len__ (self):
        return len (self.__grid)

    def __getitem__ (self, xy):
        x, y = xy
        return self.__grid [x] [y]

    def __setitem__ (self, xy, val):
        x, y = xy
        self.__new [x] [y] = val


class Engine:

    def __init__ (self, lenx, leny, init = {}, debug = True):
        """
        Create genevo engine on a (lenx, leny) grid 
        without borders and initialize it with init

        lenx, leny -- int
        init       -- dict, maps BitInt genomes to 
                            a list of two-tuple (int)
        """

        self.debug = debug

        self.gen  = 0
        self.births = 0
        self.deaths = 0
        self.mutations = 0
        self.lenx = lenx
        self.leny = leny

        self.grid = TwoSidedGrid (lenx, leny)

        for genom, pos in init.items ():
            for x, y in pos:
                self.grid [x, y] = Cell (genom)

        self.grid.flip ()

        for x in range (lenx):
            for y in range (leny):
                c = self.grid [x, y] 
                if c:
                    c.neighbours = self.find_neighbours (x, y)

        if self.debug:
            for g in init:
                c = Cell (g)
                print ("Clade", str (c.trait))
                print (
                    "Age: {} Horny: {} Mutate {} Hunger {}".format (
                        c.age, c.horny, c.mutate, c.hunger)
                )
                print (
                    "Aggro: {} Attack {}".format (
                        c.aggro, c.attack)
                )

    def find_neighbours (self, cx, cy):

        neighbours = []

        for x in (cx - 1, cx, cx + 1):
            for y in (cy - 1, cy, cy + 1):

                cell = self.grid [x % self.lenx, y % self.leny]
                if cell != None and not ( (x, y) == (cx, cy) ):
                    neighbours.append (cell)

        return neighbours

    def find_free (self, cx, cy):

        free = []
        for x in (cx - 1, cx, cx + 1):
            for y in (cy - 1, cy, cy + 1):
                if self.grid [x % self.lenx, y % self.leny] == None:
                    free.append ( (x % self.lenx, y % self.leny) )

        return random.choice (free) if free else (-1, -1)

    def count_clades (self):

        populus = {}
        for x in range (self.lenx):
            for y in range (self.leny):

                c = self.grid [x, y]
                if not c: continue
                h = c.hash (c)
                populus [h] = populus.get (h, 0) + 1

        return populus
        
    def step (self):

        if self.debug: 
            print ("Round {}".format (self.gen))
        self.gen += 1

        dead = {}
        born = {}

        for x in range (self.lenx):
            for y in range (self.leny):

                cell = self.grid [x, y]
                if cell == None:
                    continue

                cell.neighbours = self.find_neighbours (x, y)
                try:
                    cell.cycle ()
                except CellDeath as cd:
                    self.grid [x, y] = None
                    dead [x, y] = cd.args [0]
                    self.deaths += 1

                except CellBirth as cb:
                    fetus = Cell (cb.args [0])
                    self.mutations += cb.args [1]
                    bx, by = self.find_free (x, y)
                    if not bx == -1:
                        self.grid [bx, by] = fetus
                        self.births += 1
                        born [bx, by] = fetus, cb.args [1]

        self.grid.flip ()
        return dead, born

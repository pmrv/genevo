import random
from genevo.bitint import BitInt
from genevo.cell   import Cell, CellDeath, CellBirth

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

        self.make_grid ()

        for genom, pos in init.items ():
            for x, y in pos:
                self [x] [y] = Cell (genom)

        if True or self.debug:
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


    def __getitem__ (self, x):
        return self.grid [x]

    def make_grid (self):
        self.grid = [
                [None for y in range (self.leny)]
                      for x in range (self.lenx)
        ]

    def find_neighbours (self, cx, cy):

        neighbours = []

        for x in (cx - 1, cx, cx + 1):
            for y in (cy - 1, cy, cy + 1):

                cell = self [x % self.lenx] [y % self.leny]
                if cell != None and not ( (x, y) == (cx, cy) ):
                    neighbours.append (cell)

        return neighbours

    def find_free (self, cx, cy):

        free = []
        for x in (cx - 1, cx, cx + 1):
            for y in (cy - 1, cy, cy + 1):
                if self [x % self.lenx] [y % self.leny] == None:
                    free.append ( (x % self.lenx, y % self.leny) )

        return random.choice (free)

    def count_clades (self):

        populus = {}
        for x in range (self.lenx):
            for y in range (self.leny):

                c = self [x] [y]
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

                cell = self [x] [y]
                if cell == None:
                    continue

                try:
                    cell.cycle (self.find_neighbours (x, y))
                except CellDeath as cd:
                    if self.debug:
                        print ("{},{}".format (x, y), 
                               cd.args [0])
                    dead [x, y] = cd.args [0]
                except CellBirth as cb:
                    if self.debug:
                        print ("{},{} was just born.".format (x, y))
                    fetus = Cell (cb.args [0])
                    self.mutations += cb.args [1]
                    bx, by = self.find_free (x, y)
                    born [bx, by] = fetus, cb.args [1]

        for x, y in dead:
            self [x] [y] = None
            self.deaths += 1

        for (x, y), (fetus, _) in born.items ():
            self [x] [y] = fetus
            self.births += 1

        return dead, born

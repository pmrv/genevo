import random
from genevo.bitint import BitInt

class CellKill  (Exception): pass
class CellDeath (Exception): pass
class CellBirth (Exception): pass

class Cell:

    def __init__ (self, genom):
        if isinstance (genom, int):
            genom = BitInt (genom)
        elif not isinstance (genom, BitInt):
            raise ValueError ("Can't init Cell with non-int.")

        self.genom = genom
        self.age   = genom.slice (0, 4) * 16
        self.hunger= genom.slice (4, 7) %  9
        self.horny = sum (
                k * 2 ** -(i + 2) 
                    for i, k in enumerate (BitInt (genom.slice ( 9, 12)))
        )
        self.mutate = sum (
                k * 2 ** -(i + 8) 
                    for i, k in enumerate (BitInt (genom.slice (12, 16)))
        )

        self.genlen = 16
        self.attack = genom.slice (0, self.genlen, 3) # max 2**7 - 1 = 127
        self.aggro  = genom.slice (1, self.genlen, 3)
        self.trait  = self.hash (self)

        self.neighbours = [] # list of all neighbours

    @staticmethod
    def hash (cell):
        g  = cell.genom
        lg = cell.genlen
        return g.slice (0, lg, 2) | g.slice (1, lg, 2)

    def checkout (self, mate):
        if self.trait == mate.trait:
            return True
        m = BitInt (self.trait ^ mate.trait)
        return (m.bits () / 8) < (self.mutate * 100)

    def mutate_mask (self):
        if random.random () < (self.mutate + .01):
            mut1 = random.getrandbits (16)
            mut2 = random.getrandbits (16)
            mut3 = random.getrandbits (16)
            return (mut1 ^ mut2) & mut3

        return 0

    def mate (self, mate):

        gens = (self.genom, mate.genom)
        # recombine genomes
        new = sum (gens [random.randint (0, 1)].slice (i, i + 4) << i 
                for i in range (0, self.genlen, 4))

        mask = self.mutate_mask ()
        return BitInt (new ^ mask), bool (mask)

    def clone (self):

        mask = self.mutate_mask ()
        return BitInt (self.genom.base ^ mask), bool (mask)

    def cycle (self):

        if getattr (self, "murdered", False): # have been murdered by another cell
            raise CellDeath ("Was murdered.")

        self.age -= 1
        if self.age < 0:
            raise CellDeath ("Died of age.")

        mood = random.random () < (self.horny + .001) # whether we are in 'the mood right now'

        neighbours = self.neighbours
        lneigh = len (neighbours)
        if lneigh > 0:
            mhunger = sum (n.hunger for n in neighbours) / lneigh

            mates  = []
            fiends = []
            # Alternative, nicer but probably slower:
            # mates, fiends = itertools.groupby (neighbours.sort (self.checkout), self.checkout).values ()
            for n in neighbours:
                if self.checkout (n):
                    mates.append (n)
                else:
                    fiends.append (n)

            if fiends and mhunger > 0 and lneigh / mhunger * 128 > self.aggro:
                opponent = random.choice (fiends)
                if self.attack >= opponent.attack:
                    opponent.murdered = True
                    return # won't starve if we just killed another cell (and eat it)
                else:
                    raise CellDeath ("Was murdered.")

            if mhunger < lneigh:
                raise CellDeath ("Starved.")

            # if we have 8 neighbours, there'd be no room for our child
            if mood and lneigh < 8 and mates:
                raise CellBirth (*self.mate (random.choice (mates)))
        elif mood:
            raise CellBirth (*self.clone ())


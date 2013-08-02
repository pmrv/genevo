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

        self.alive = True # used for fighting
        self.genom = genom
        self.age = 1 << genom [:2] + 1 << (2 + genom [2:4])
        self.hunger = (genom [4:7]  - 2) % 9
        self.horny = sum (
                k * 2 ** -(i + 3) for i, k in enumerate (genom [ 9:12])
        )
        self.mutate = sum (
                k * 2 ** -(i + 4) for i, k in enumerate (genom [12:16])
        )

        self.attack = genom [::3] # max 2**7 - 1 = 127
        self.aggro  = genom [1::3]
        self.trait  = self.hash (self)

        self.neighbours = [] # list of all neighbours

    @staticmethod
    def hash (cell):
        g = cell.genom
        return BitInt (g [::2] ^ g [1::2])

    def checkout (self, mate):
        if self.trait == mate.trait:
            return True
        m = BitInt (~(self.trait ^ mate.trait))
        return (m.bitcount () / 16) < (self.mutate * 10)

    def mate (self, mate):

        seg = lambda i: random.choice (
                (self.genom [i:i + 4], mate.genom [i:i + 4])
        )
        # recombine genomes
        new = sum (seg (i) << i for i in range (0, 16, 4))

        mutated = random.random () < (self.mutate + .01)
        if mutated:
            mut1 = random.getrandbits (16)
            mut2 = random.getrandbits (16)
            mut3 = random.getrandbits (16)
            new ^= (mut1 ^ mut2) & mut3
        
        return BitInt (new), mutated

    def cycle (self):

        if not self.alive: # have been murdered by another cell
            raise CellDeath ("Was murdered.")

        self.age -= 1
        if self.age < 0:
            raise CellDeath ("Died of age.")

        neighbours = self.neighbours
        lneigh = len (neighbours)
        if lneigh > 0:
            mhunger = sum (n.hunger for n in neighbours) / lneigh
            if mhunger > 0 and lneigh / mhunger * 128 > self.aggro:
                opponent = random.choice (neighbours)
                if not self.checkout (opponent): # leave our own kind alone
                    if self.attack >= opponent.attack:
                        opponent.alive = False
                        return
                    else:
                        raise CellDeath ("Was murdered.")

            if mhunger < lneigh:
                raise CellDeath ("Starved.")

        # if we have 8 neighbours, there'd be no room for our child
        if 0 < lneigh < 8 and random.random () < (self.horny + .01):
            mates = list (
                    filter (self.checkout, neighbours))
            if len (mates) > 0:
                raise CellBirth (*self.mate (random.choice (mates)))

import math

class BitInt (int):

    def bitcount (self):
        if   self ==  0:
            return 0
        
        l = len (self)
        v = self
        c = 0
        while v != 0 and c < l:
            v &= v - 1
            c += 1

        return c

    def __len__ (self):
        if self == 0: return 0
        return round (math.log (abs (self), 2) + .5)

    def __iter__ (self):
        return (self [i] for i in range (len (self)))

    def __getitem__ (self, i):
        if not isinstance (i, slice):
            return (self & (1 << i)) // (1 << i)
        
        a = i.start
        b = i.stop
        s = i.step

        if i.start == None:
            a = 0
        if i.stop  == None:
            b = len (self)

        if i.step == None:
            return BitInt (( self % (1 << b) ) // (1 << a))

        if i.step < 0:
            t = a
            a = b
            b = t
            s = abs (s)

        if a >= b:
            return BitInt (0)

        z = 0
        for k in range (a, b, s):
            z += self % (1 << k + 1) >> k << (k // s)

        return BitInt (z >> (a // s))

    def __str__ (self):
        return bin (self)

    def __repr__ (self):
        return "BitInt (%i)" % self

from libc.math cimport ilogb, abs

cdef class BitInt:

    cdef readonly base

    def __init__ (self, int base):
        self.base = base


    cpdef int bits (self):
        if self.base == 0:
            return 0
        
        cdef int l = len (self)
        cdef int v = self.base
        cdef int c = 0
        while v != 0 and c < l:
            v &= v - 1
            c += 1

        return c

    def __len__ (self):
        if self.base == 0: return 0
        return ilogb (self.base) + 1

    def __iter__ (self):
        return (self.get (i) for i in range (len (self)))

    cpdef int get (self, int i):
        return (self.base & (1 << i)) // (1 << i)

    cpdef int slice (self, int a, int b, int s = 1):

        if s == 1:
            return ( self.base % (1 << b) ) // (1 << a)

        if s < 0:
            a, b = b, a
            s = abs (s)

        if a >= b:
            return 0

        z = 0
        for k in range (a, b, s):
            z += self.base % (1 << k + 1) >> k << (k // s)

        return z >> (a // s)

    def __str__ (self):
        return bin (self.base)

    def __repr__ (self):
        return "BitInt (%s)" % str (self)

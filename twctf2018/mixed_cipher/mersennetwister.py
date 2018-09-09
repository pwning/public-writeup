"""A generalized Mersenne Twister module.

Provides a MersenneTwister class, and a MT19937 class which
instantiates MersenneTwister with the appropriate standard constants
used for MT19937.

Reference Pseudocode taken from https://en.wikipedia.org/wiki/Mersenne_Twister

"""


def _low_bits(k, n):
    """Return lowest k bits of n."""
    return (((1 << k) - 1) & n)


class MersenneTwister:
    """A generalized Mersenne Twister class.

    Example usage:

    >>> mt = MersenneTwister(...).seed(0)
    >>> mt.next()

    """

    def __init__(self, w, n, m, r, a, u, d, s, b, t, c, l, f):
        """Set up internal state to say that it is not seeded."""
        self.MT = [0]*n
        self.index = n+1
        self.lower_mask = (1 << r) - 1
        self.upper_mask = _low_bits(w, ~ self.lower_mask)
        self.w = w
        self.n = n
        self.m = m
        self.r = r
        self.a = a
        self.u = u
        self.d = d
        self.s = s
        self.b = b
        self.t = t
        self.c = c
        self.l = l
        self.f = f

    def seed(self, seed):
        """Initialize the generator from the seed."""
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = _low_bits(self.w,
                                   (self.f *
                                    (self.MT[i-1] ^
                                     (self.MT[i-1] >> (self.w-2))) + i))

    def twist(self):
        """Generate the next n values from the series x_i.

        This is mainly meant for internal usage. Not to be used
        externally unless you know what you are doing.

        """
        for i in range(self.n):
            x = ((self.MT[i] & self.upper_mask) +
                 (self.MT[(i+1) % self.n] & self.lower_mask))
            xA = (x >> 1)
            if x % 2 != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def _temper(self, y):
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        return _low_bits(self.w, y)

    def next(self):
        """Extract a tempered value based on MT[index].

        Calls twist() every n numbers.

        """
        if self.index >= self.n:
            if self.index > self.n:
                print "Generator was never seeded"
            self.twist()

        ret = self._temper(self.MT[self.index])
        self.index += 1
        return ret

    def _untemper(self, y):
        """Untemper value to get internal state."""
        def rev_shxor(y, word, rsh, mask):
            """Reverse the tempering shift-and-xor operation.

            Finds x for the equation: y = x ^ ((x >> rsh) & d)

            Note: rsh is allowed to be either positive (right-shift),
            or negative (left-shift).

            word is the number of bits that x and y are allowed to
            have.

            """
            def _rshift(a, rsh):
                if rsh > 0:
                    return a >> rsh
                else:
                    return a << (-rsh)

            def get_bit(b):
                """Get the b'th bit counting from LSB=0."""
                if b < 0 or b >= word:
                    return 0
                elif mask & (1 << b) == 0:
                    return y & (1 << b)
                else:
                    return (y & (1 << b)) ^ (_rshift(get_bit(b + rsh),
                                                     rsh))

            return sum(get_bit(b) for b in range(word))

        y = rev_shxor(y, self.w, self.l, (1 << self.w) - 1)
        y = rev_shxor(y, self.w, -self.t, self.c)
        y = rev_shxor(y, self.w, -self.s, self.b)
        y = rev_shxor(y, self.w, self.u, self.d)
        return y

    def seed_via_clone(self, values):
        """Seed the twister via cloning another twister.

        This takes a list of n values which are outputs from another
        twister with the same coefficients (i.e., w, n, m, r, a, u, d,
        s, b, t, c, l, f), but with some unknown seed. It uses these
        values to create a clone of the other twister, so that both
        twisters will start to give same output.

        This works because the tempering function is a bijective
        function and can efficiently be inverted (see _untemper) to
        get the internal state of the twister.

        """
        assert(type(values) is list)
        assert(len(values) == self.n)

        for i, v in enumerate(values):
            self.MT[i] = self._untemper(v)

        self.index = self.n


class MT19937:
    """Generate a MT19937 Mersenne Twister."""

    def __init__(self, seed=None):
        """Initialize with a seed (if provided)."""
        w = 32
        n = 624
        m = 397
        r = 31
        a = 0x9908B0DF
        u = 11
        d = 0xFFFFFFFF
        s = 7
        b = 0x9D2C5680
        t = 15
        c = 0xEFC60000
        l = 18
        f = 1812433253
        self.mt = MersenneTwister(w, n, m, r, a, u, d, s, b, t, c, l, f)
        if seed is not None:
            self.mt.seed(seed)

    def seed(self, seed):
        """Initialize the generator from the seed."""
        self.mt.seed(seed)

    def seed_via_clone(self, values):
        """Seed the twister via cloning another MT19937.

        See MersenneTwister.seed_via_clone for more details.
        """
        self.mt.seed_via_clone(values)

    def next(self):
        """Generate next value."""
        return self.mt.next()

if __name__ == '__main__':
    assert(MT19937(0).next() == 2357136044)
    assert(MT19937(0x6a6179).next() == 225179560)

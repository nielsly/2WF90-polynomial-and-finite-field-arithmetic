from random import randint

known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


class Poly:
    # initialise the Poly, inputs can be int, list or string
    # modulus must be a prime int or 0, if it is 0 then we don't ever reduce the numbers
    # degree is used if a single integer/empty string is entered
    def __init__(self, a: int or list or str, m: int = 0, degree=0):
        # simple prime check for the modulo. We use a pre-generated list of primes, since we know p < 100:
        if m != 0 and m not in known_primes:
            raise ValueError("Modulus is not prime")

        self.m: int = m
        if type(a) == str:
            a = a.split(' ')
            if len(a) == 1:
                if a[0].startswith('-'):
                    a = '-' + ' - '.join(' + '.join(a[0][1:].split('+')).split('-'))
                else:
                    a = ' - '.join(' + '.join(a[0].split('+')).split('-'))
            a = a.split(' ')
            spl = a[0].split('^')
            if len(spl) > 1:
                degree = int(spl[1])
            elif spl[0].endswith('X'):
                degree = 1
            p = [0] * (degree + 1)
            if spl[0].endswith('X'):
                if spl[0] == '-X':
                    p[0] = -1
                elif spl[0] == 'X':
                    p[0] = 1
                else:
                    p[0] = int(spl[0][:-1])
            else:
                p[0] = int(spl[0])
            for i in range(2, len(a), 2):
                if a[i - 1] == '-':
                    a[i] = '-' + a[i]
                spl = a[i].split('^')
                if spl[0].endswith('X'):
                    if spl[0] == '-X':
                        if len(spl) == 1:
                            p[degree - 1] = 1 if a[i - 1] == '+' else -1
                        else:
                            p[degree - int(spl[1])] = 1 if a[i - 1] == '+' else -1
                    elif spl[0] == 'X':
                        if len(spl) == 1:
                            p[degree - 1] = 1 if a[i - 1] == '+' else -1
                        else:
                            p[degree - int(spl[1])] = 1 if a[i - 1] == '+' else -1
                    else:
                        if len(spl) == 1:
                            p[degree - 1] = int(spl[0][:-1]) if a[i - 1] == '+' else int('-' + spl[0][:-1])
                        else:
                            p[degree - int(spl[1])] = int(spl[0][:-1]) if a[i - 1] == '+' \
                                else int('-' + spl[0][:-1])
                else:
                    p[degree] = int(spl[0]) if a[i - 1] == '+' else int('-' + spl[0])
            self.data: list = p
        elif type(a) == int:
            if degree < 0:
                raise ValueError('When declaring a Poly with an int, a non-negative degree is also required.')
            self.data: list = [0] * (degree + 1)
            self.data[0] = a
        elif type(a) == list:
            if m != 0:
                for i in range(len(a)):
                    a[i] %= m
            self.data: list = a
            self.trim()
        else:
            raise TypeError('Type Poly requires type str, int or list, not ' + str(type(a)))

    # degree of poly
    def deg(self) -> int:
        # return (length of data - index of first non-zero element) - 1
        for i, e in enumerate(self.data):
            if e != 0:
                return len(self.data) - i - 1
        # return -1 if Poly = 0
        return -1

    # leading coefficient
    def lc(self) -> int:
        # return first non-zero element
        for n in self.data:
            if n != 0:
                return n
        # return 0 if Poly = 0
        return 0

    # string representation of poly, has spaces
    def __str__(self, spaces=False) -> str:
        degree = self.deg()
        self.data.reverse()
        out = ""
        for i in range(degree, -1, -1):
            n = self.data[i]
            if n != 0:
                if n > 0 and i != degree:
                    if spaces:
                        out += " + "
                    else:
                        out += "+"
                elif n < 0:
                    if i == degree or not spaces:
                        out += "-"
                    else:
                        out += " - "
                if abs(n) != 1 or i == 0:
                    out += str(abs(n))
                if i > 0:
                    out += "X"
                    if i > 1:
                        out += "^" + str(i)
        self.data.reverse()
        return out if out != "" else str(0)

    # representation when printing to console
    def __repr__(self):
        return str(self)

    # * for poly
    def __mul__(self, other):
        if type(other) == int:
            other = Poly(other, self.m)

        n = len(self)
        m = len(other)
        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        length = n + m - 1
        p = [0] * length
        for i in range(n):
            for j in range(m):
                if ap[i] != 0 and bp[j] != 0:
                    p[i + j] += ap[i] * bp[j]
        p.reverse()
        return Poly(p, self.m)

    # + for poly
    def __add__(self, other):
        if type(other) == int:
            other = Poly(other, self.m)

        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        while len(ap) - 1 < other.deg():
            ap.append(0)
        for i in range(other.deg() + 1):
            ap[i] += bp[i]
        ap.reverse()
        return Poly(ap, self.m)

    # - for poly
    def __sub__(self, other):
        if type(other) == int:
            other = Poly(other, self.m)

        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        while len(ap) - 1 < other.deg():
            ap.append(0)
        for i in range(other.deg() + 1):
            ap[i] -= bp[i]
        ap.reverse()
        return Poly(ap, self.m)

    # make copy of poly
    def copy(self):
        return Poly(self.data, self.m)

    # modular long division for polynomials
    # based on algorithm 2.2.6 of the reader with adjustments made for modular arithmetic
    def __truediv__(self, other):
        if type(other) == int:
            other = Poly(other, self.m)

        if other == 0:
            raise ZeroDivisionError("Division by zero attempted on " + str(self) + " and " + str(other) + ".")

        q = [0] * len(self)
        r = self.copy()
        deg_r, deg_b = r.deg(), other.deg()

        while deg_r >= deg_b:
            # We need to eliminate the highest order coefficient
            # We can safely loop through all possibilities, since we know that m < 100
            lc_div = 1
            for i in range(1, self.m + 1):
                if (r.lc() - i * other.lc()) % self.m == 0:
                    lc_div = i
                    break

            q[deg_r - deg_b] += lc_div
            n = Poly(lc_div, self.m, deg_r - deg_b)
            nb = n * other
            r = (r - nb) % self.m
            deg_r = r.deg()
        q.reverse()
        return Poly(q, self.m), r.trim()

    # gcd of two polynomials, uses euclid's extended algorithm under the hood
    def gcd(self, other):
        return self.euclid(other)[2]

    # extended euclidean algorithm for polynomials
    # Based on algorithm 2.2.11 from the script
    def euclid(self, other):
        x, v, y, u = Poly(1, self.m), Poly(1, self.m), Poly(0, self.m), Poly(0, self.m)
        a, b = self.copy(), other.copy()
        while b > 0:
            q, r = a / b
            a = b
            b = r
            xp = x
            yp = y
            x = u
            y = v
            u = xp - q * u
            v = yp - q * v

        a_inv = modular_inverse(a.lc(), self.m, True)
        a = x * a_inv
        b = y * a_inv
        return a, b, self * a + other * b

    def __len__(self) -> int:
        # return length of data - index of first non-zero element
        for i, e in enumerate(self.data):
            if e != 0:
                return len(self.data) - i
        # return 1 if Poly = 0
        return 1

    # remove leading zeroes
    def trim(self):
        self.data = self.data[len(self.data) - len(self):]
        if len(self.data) == 0:
            self.data = [0]
        return self

    # % for poly, currently only works with ints
    def __mod__(self, m):
        if type(m) == int:
            if m != 0:
                a = self.data.copy()
                for i in range(len(a)):
                    a[i] %= m
                return Poly(a, self.m)
            else:
                # the polynomial taken mod 0 gives the polynomial itself
                return self
        elif type(m) == Poly:
            degm = m.deg() + 1
            if degm == 0:
                # apparently Poly a m (Poly b = 0) = Poly a
                return self
            # if len(self.data) < degm:
            #     return Poly(self.data, self.m) % self.m
            # m.trim()
            # # lc*x^(degm) + (bx^j + ... + c) = 0 => lc*x^(degm) = -bx^j - ... - c
            # lcm = m.lc()
            #
            # # shift everything except lc to right hand side
            # rhs = m.data[1:]
            #
            # # lc * x ^ (degm) = -bx ^ j - ... - c => x^(degm) -b/lc * x^j - ... - c/lc
            # for i in range(len(rhs)):
            #     rhs[i] = 0 - rhs[i] // lcm
            #
            # # get poly as list
            # data = self.data
            # # get everything to the right of x^(degm) term
            # output = Poly(self.data[-degm + 1:], self.m)
            # # get everything else to get x^(degm) (f*x^(deg-1) + ... + g)
            # rest = data[:-degm + 1]
            #
            # # Create a step poly before the loop and adjust its data instead of creating a new
            # # one each iteration (saves ~0.4 seconds):
            # stepPoly = Poly([0], self.m)
            # # for each term in the rest get product with rhs for substitution
            # for i in range(len(rest)):
            #     step = rhs.copy()
            #     # for each term in rhs
            #     for j in range(len(step)):
            #         # get product
            #         step[j] *= rest[i]
            #     # pad with zeroes to match degree of term
            #     step += [0] * (len(rest) - i - 1)
            #     stepPoly.data = step
            #     # add step to current answer
            #     output += stepPoly
            #
            # # recurse if still not fully reduced
            # if output.deg() >= m.deg():
            #     return output % m
            # # else return with reduced terms
            # return output % self.m
            return (self.copy() / m)[1]

    # < for poly
    def __lt__(self, other) -> bool:
        if type(other) == int:
            other = Poly(other, self.m)
        return other > self

    # <= for poly
    def __le__(self, other) -> bool:
        if type(other) == int:
            other = Poly(other, self.m)
        return other >= self

    # > for poly
    def __gt__(self, other) -> bool:
        if type(other) == int:
            other = Poly(other, self.m)
        s = self.copy()
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            return False
        elif deg_o < deg_s:
            return True
        s -= other % self.m
        return s.lc() > 0

    # >= for poly
    def __ge__(self, other) -> bool:
        if type(other) == int:
            other = Poly(other, self.m)
        s = self.copy()
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            return False
        elif deg_o < deg_s:
            return True
        s -= other % self.m
        return s.lc() >= 0

    # != for poly
    def __ne__(self, other) -> bool:
        if type(other) == int:
            other = Poly(other, self.m)
        return not self == other

    # == for poly
    def __eq__(self, other) -> bool:
        if type(other) == int:
            other = Poly(other, self.m)
        s = self.copy()
        s -= other % self.m
        return s.lc() == 0

    # power for poly with n being an integer
    def pow(self, n: int):
        x = self.copy()
        z = Poly('1', self.m)
        if n == 0:
            return Poly('1', self.m)
        if self.m == 0:
            while n > 1:
                if n % 2 == 1:
                    z *= x
                    n -= 1
                x *= x
                n /= 2
            return z * x
        else:
            while n > 1:
                if n % 2 == 1:
                    z = (z * x) % self.m
                    n -= 1
                x = (x * x) % self.m
                n /= 2
            return (z * x) % self.m

    def poly_mod_eq(self, other, m) -> bool:
        return self % m == other % m

    # Check if polynomial is irreducible.
    # Based on algorithm 5.1.4, but with a for-loop to prevent infinite loops
    def irreducible(self) -> bool:
        f = self
        m = f.m
        for t in range(1, f.deg()):
            if f.gcd(Poly('X^{}-X'.format(m * t), m)) != Poly([1], m):
                return False
        return True

    # def shift_first_element(self, d):
    #     deg = len(self) - 1
    #     if d < deg:
    #         raise ValueError('d must be larger than current degree')
    #     self.data.reverse()
    #     for i in range(deg - d):
    #         self.data.append(0)
    #     self.data[-1], self.data[deg] = self.data[deg], 0
    #     self.data.reverse()
    #
    #     def irreducible(self):
    #         q = self.m
    #         poly = Poly("X^" + str(self.m) + "-X", self.m)
    #         for t in range(1, self.deg()):
    #             if self.gcd(poly) != Poly(1, self.m):
    #                 return False
    #             poly.shift_first_element(q * t)
    #         return True


# modular inverse of an integer
def modular_inverse(n: int, m, return_poly=False) -> Poly or int:
    assert (n != 0 and m > 0)

    for i in range(1, m + 1):
        if (i * n) % m == 1:
            if return_poly:
                return Poly(i, m)
            else:
                return i
    raise AssertionError


# Find irreducible polynomial of degree n in Z/modZ
def find_irred(m: int, deg: int, give_all=True) -> list or Poly:
    if deg < 0:
        raise ValueError('Degree must 0 or higher')

    found_polys = []
    data = [0] * (deg + 1)
    for n in range(1, m):
        data[0] = n
        poly = Poly(data, m)
        found = find_irred_step(poly, deg)
        if len(found) > 0:
            found_polys += found
    if len(found_polys) == 0:
        raise ValueError('No such polynomial exists')

    # the code above may give duplicates, we remove these
    output_polys = []
    for x in found_polys:
        if x not in output_polys:
            output_polys.append(x)
    if give_all:
        return output_polys
    return output_polys[randint(0, len(output_polys) - 1)]


def find_irred_step(poly: Poly, d: int) -> list:
    found_polys = []
    if poly.irreducible():
        found_polys.append(poly)
    if d == 0:
        return found_polys
    for n in range(0, poly.m):
        new_poly = poly.copy()
        new_poly.data[d] = n
        found = find_irred_step(new_poly, d - 1)
        if len(found) > 0:
            found_polys += found
    return found_polys


# print(Poly('6X^5+5X^3+5X^2+2X+2', 3))
# print(Poly('X^2+X', 5).pow(15))
# print(Poly('X^7') <= Poly('X^2'))
# print(Poly('X^2') != Poly('X^2'))
# print(Poly([1,0,1]).euclid(Poly([1,0,0,1])))
# test = Poly('X^5+4X^3+X^2+X+1', 5)
# testm = Poly('X^3-X+2', test.m)
# print(test % testm)


# print(Poly('X^3-X+2').trim(), Poly([0,0,0,10,2,0,1]))

# print(Poly('X^4+X^3+1', 2).irreducible())

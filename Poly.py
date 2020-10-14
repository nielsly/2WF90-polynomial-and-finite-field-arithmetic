class Poly:
    # initialise the Poly, intputs can be int, list or string, degree is used if a single integer or empty string is entered
    def __init__(self, a: int or list or str, degree: int = 0):
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
                            p[degree - 1] = -1 if a[i - 1] == '+' else 1
                        else:
                            p[degree - int(spl[1])] = 1 if a[i - 1] == '+' else 1
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
            self.data = p
            self.degree = len(p)
        elif type(a) == int:
            if degree < 0:
                raise ValueError('When declaring a Poly with an int, a non-negative degree is also required.')
            self.data = [0] * (degree + 1)
            self.data[0] = a
            self.degree = degree
        elif type(a) == list:
            self.data = a
            self.degree = degree
        else:
            raise TypeError('Type Poly requires type str, int or list, not ' + str(type(a)))

    # degree of poly
    def deg(self):
        if self.degree == len(self.data) and self.data[0] != 0:
            return self.degree
        for i, e in enumerate(self.data):
            if e != 0:
                return len(self.data) - i
        return 1

    # leading coefficient
    def lc(self):
        for n in self.data:
            if n != 0:
                return n
        return 0

    # string representation of poly, has spaces
    def __str__(self):
        degree = self.deg()
        self.data.reverse()
        out = ""
        for i in range(degree - 1, -1, -1):
            n = self.data[i]
            if n != 0:
                if n > 0 and i != degree - 1:
                    out += " + "
                elif n < 0:
                    if i == degree - 1:
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
        n = self.deg()
        m = other.deg()
        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        degree = n + m
        p = [0] * degree
        for i in range(n):
            for j in range(m):
                if ap[i] != 0 and bp[j] != 0:
                    p[i + j] += ap[i] * bp[j]
        p.reverse()
        return Poly(p).trim()

    # + for poly
    def __add__(self, other):
        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        while len(ap) < other.deg():
            ap.append(0)
        for i in range(other.deg()):
            ap[i] += bp[i]
        ap.reverse()
        return Poly(ap)

    # - for poly
    def __sub__(self, other):
        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        while len(ap) < other.deg():
            ap.append(0)
        for i in range(other.deg()):
            ap[i] -= bp[i]
        ap.reverse()
        return Poly(ap).trim()

    # make copy of poly
    def copy(self):
        return Poly(self.data)

    # / for poly
    def __truediv__(self, other):
        q = [0] * (self.deg() + other.deg())
        r = self.copy()
        deg_r, deg_b = r.deg(), other.deg()
        while r > Poly(0) and deg_r >= deg_b:
            lc_div = r.lc() // other.lc()
            q[deg_r - deg_b] += lc_div
            n = Poly(lc_div, deg_r - deg_b)
            nb = n * other
            r = r - nb
            deg_r = r.deg()
        q.reverse()
        return Poly(q).trim(), r

    # gcd of poly and other poly, doesnt work due to floats i think
    def gcd(self, other):
        a = self.copy()
        b = other.copy()
        while b.deg() > 0:
            b, a = a - b, b
        return Poly(1 / a.lc())

    # extended euclidean algorithm for poly
    def euclid(self, other):
        x, v, y, u = Poly(1), Poly(1), Poly(0), Poly(0)
        a, b = self.copy(), other.copy()
        while b > Poly(0):
            q, r = a / b
            a = b
            b = r
            xp = x
            yp = y
            x = u
            y = v
            u = xp - q * u
            v = yp - q * v
        lca = 1 / a.lc()
        return x * lca, y * lca

    # length of poly, includes leading zeroes, whereas deg() does not
    def __len__(self):
        return len(self.data)

    # remove leading zeroes
    def trim(self):
        self.data = self.data[len(self.data) - self.deg():]
        if len(self.data) == 0:
            self.data = [0]
        return self

    # % for poly, currently only works with ints
    def __mod__(self, other):
        a = self.data.copy()
        m = other
        for i in range(len(a)):
            while a[i] < 0:
                a[i] += m
            while a[i] >= m:
                a[i] -= m
        return Poly(a)

    # < for poly
    def __lt__(self, other):
        return other > self

    # <= for poly
    def __le__(self, other):
        return other >= self

    # > for poly
    def __gt__(self, other):
        s = self.copy()
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            return False
        elif deg_o < deg_s:
            return True
        s -= other
        return s.lc() > 0

    # >= for poly
    def __ge__(self, other):
        s = self.copy()
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            return False
        elif deg_o < deg_s:
            return True
        s -= other
        return s.lc() >= 0

    # != for poly
    def __ne__(self, other):
        return not self == other

    # == for poly
    def __eq__(self, other):
        s = self.copy()
        s -= other
        return s.lc() == 0

    # power for poly
    # m is een integer hier, niet een polynomial, polynomial mod nog implementen
    def pow(self, n: int, m=0):
        x = self.copy()
        z = Poly('1')
        if n == 0:
            return Poly('1')
        if m == 0:
            while n > 1:
                if n % 2 == 1:
                    z *= x
                    n -= 1
                x *= x
                n /= 2
            return z*x
        else:
            while n > 1:
                if n % 2 == 1:
                    z = z * x % m
                    n -= 1
                x = x * x % m
                n /= 2
            return z * x % m

    # def shift_first_element(self, d):
    #     deg = self.deg()
    #     if d < deg:
    #         raise ValueError('d must be larger than current degree')
    #     self.data.reverse()
    #     for i in range(deg - d):
    #         self.data.append(0)
    #     self.data[-1], self.data[deg] = self.data[deg], 0
    #     self.data.reverse()
    #
    # def irreducible(self):
    #     q = 0 # ???????
    #     print('X^' + str(q) + ' - X')
    #     x = Poly('X^' + str(q) + ' - X')
    #     t = 1
    #     while self.gcd(x) == 1:
    #         x.shift_first_element(q)
    #         t += 1
    #     return t == q


print(Poly('6X^5+5X^3+5X^2+2X+2'))
print(Poly('X^2+X').pow(15, 5))
print(Poly('X^7') <= Poly('X^2'))
print(Poly('X^2') != Poly('X^2'))
# print(Poly([1,0,1]).euclid(Poly([1,0,0,1])))
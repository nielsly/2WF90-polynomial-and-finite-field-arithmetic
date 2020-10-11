class Fraction:
    def __init__(self, n, d=1):
        if type(n) == str:
            n = n.split('/')
            self.n = int(n[0])
            if len(n) > 1:
                self.d = int(n[1])
            else:
                self.d = 1
        elif type(n) == int:
            if type(d) == int:
                self.n = n
                self.d = d
            else:
                self.n = d.d * n
                self.d = d.n
        elif type(d) == int:
            self.n = n.n
            self.d = n.d * d
        elif type(d) == Fraction:
            self.n = n.n * d.d
            self.d = n.d * d.n
        else:
            raise TypeError('Fraction only accepts str or int int, not' + str(type(n)) + " " + str(type(d)))
        if self.d == 0:
            raise ZeroDivisionError('You cannot divide by 0')
        if self.d < 0:
            self.d = abs(self.d)
            self.n = 0 - self.n
        self.reduce()

    def __add__(self, other):
        s = self.copy()
        if type(other) == int:
            s.n += s.d * int(other)
        elif type(other) == Fraction:
            if other.n == 0:
                return s
            elif s.n == 0:
                return other
            if s.d < other.d:
                d = other.gcd(s)
            else:
                d = s.gcd(other)
            d = (s.d * other.d) // d
            s.n = s.n * (d // s.d) + other.n * (d // other.d)
            s.d = d
        else:
            raise TypeError('Type Fraction requires type int or Fraction, not ' + str(type(other)))
        return s.reduce()

    def __sub__(self, other):
        s = self.copy()
        if type(other) == int:
            other = 0 - other
        elif type(other) == Fraction:
            other.n = 0 - other.n
        else:
            raise TypeError('Type Fraction requires type int or Fraction, not ' + str(type(other)))
        return s + other

    def __mul__(self, other):
        p = self.copy()
        if type(other) == int:
            p.n *= other
        elif type(other) == Fraction:
            p.n *= other.n
            p.d *= other.d
        else:
            raise TypeError('Type Fraction requires type int or Fraction, not ' + str(type(other)))
        return p.reduce()

    def __truediv__(self, other):
        q = self.copy()
        if type(other) == int:
            if q.n % other == 0:
                q.n //= other
            else:
                q.d *= other
        elif type(other) == Fraction:
            q.n *= other.d
            q.d *= other.n
        else:
            raise TypeError('Type Fraction requires type int or Fraction, not ' + str(type(other)))
        return q.reduce()

    def __str__(self):
        self.reduce()
        if self.n == self.d:
            return str(1)
        elif self.n == 0:
            return str(0)
        elif self.d == 1:
            return str(self.n)
        return str(self.n) + "/" + str(self.d)

    def strl(self):
        self.reduce()
        if self.n == self.d:
            return str(1)
        elif self.n == 0:
            return str(0)
        elif self.d == 1:
            return str(self.n)
        return '\\frac{' + str(self.n) + "}{" + str(self.d) + '}'

    def __repr__(self):
        return str(self)

    def reduce(self):
        if self.d == self.n:
            self.n = 1
            self.d = 1
        else:
            d = self.gcd()
            self.n //= d
            self.d //= d
        return self

    def __lt__(self, other):
        s = self.copy()
        return (s - other).n < 0

    def __le__(self, other):
        s = self.copy()
        return (s - other).n <= 0

    def __gt__(self, other):
        s = self.copy()
        return (s - other).n > 0

    def __ge__(self, other):
        s = self.copy()
        return (s - other).n >= 0

    def __float__(self):
        if self.d == 0:
            return float('Inf')
        return self.n / self.d

    def __ne__(self, other):
        s = self.copy()
        return (s - other).n != 0

    def __eq__(self, other):
        s = self.copy()
        return (s - other).n == 0

    def __abs__(self):
        s = self.copy()
        s.n = abs(s.n)
        s.d = abs(s.d)
        return s

    def __len__(self):
        return 1

    def copy(self):
        return Fraction(self)

    def gcd(self, other=0):
        if type(other) == Fraction:
            x, y = self.d, other.d
        else:
            x, y = self.n, self.d
        while y:
            x, y = y, x % y
        return x

class Polynomial:
    def __init__(self, a: int or Fraction or list or str, degree: int = 0):
        if type(a) == str:
            degree = 0
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
            p = [Fraction(0)] * (degree + 1)
            if spl[0].endswith('X'):
                if spl[0] == '-X':
                    p[0] = Fraction(-1)
                elif spl[0] == 'X':
                    p[0] = Fraction(1)
                else:
                    p[0] = Fraction(spl[0][:-1])
            else:
                p[0] = Fraction(spl[0])
            for i in range(2, len(a), 2):
                if a[i - 1] == '-':
                    a[i] = '-' + a[i]
                spl = a[i].split('^')
                if spl[0].endswith('X'):
                    if spl[0] == '-X':
                        if len(spl) == 1:
                            p[degree - 1] = Fraction(-1) if a[i - 1] == '+' else Fraction(1)
                        else:
                            p[degree - int(spl[1])] = Fraction(1) if a[i - 1] == '+' else Fraction(1)
                    elif spl[0] == 'X':
                        if len(spl) == 1:
                            p[degree - 1] = Fraction(1) if a[i - 1] == '+' else Fraction(-1)
                        else:
                            p[degree - int(spl[1])] = Fraction(1) if a[i - 1] == '+' else Fraction(-1)
                    else:
                        if len(spl) == 1:
                            p[degree - 1] = Fraction(spl[0][:-1]) if a[i - 1] == '+' else Fraction('-' + spl[0][:-1])
                        else:
                            p[degree - int(spl[1])] = Fraction(spl[0][:-1]) if a[i - 1] == '+' \
                                else Fraction('-' + spl[0][:-1])
                else:
                    p[degree] = Fraction(spl[0]) if a[i - 1] == '+' else Fraction('-' + spl[0])
            self.data = p
            self.degree = len(p)
        elif type(a) == int:
            if degree < 0:
                raise ValueError('When declaring a Polynomial with an int, a non-negative degree is also required.')
            self.data = [Fraction(0)] * (degree + 1)
            self.data[0] = Fraction(a)
            self.degree = degree
        elif type(a) == Fraction:
            if degree < 0:
                raise ValueError('When declaring a Polynomial with a Fraction, a non-negative degree is also required.')
            self.data = [Fraction(0)] * (degree + 1)
            self.data[0] = a
            self.degree = degree
        elif type(a) == list:
            for i in range(len(a)):
                if type(a[i]) != Fraction:
                    a[i] = Fraction(a[i])
            self.data = a
            self.degree = degree
        else:
            raise TypeError('Type Polynomial requires type int, Fraction or list, not ' + str(type(a)))

    def strl(self):
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
                    out += abs(n).strl()
                if i > 0:
                    out += "X"
                    if i > 1:
                        out += "^" + str(i)
        self.data.reverse()
        return out if out != "" else str(0)

    def deg(self):
        if self.degree == len(self.data) and self.data[0] != Fraction(0):
            return self.degree
        for i, e in enumerate(self.data):
            if e != 0:
                return len(self.data) - i
        return 0

    def lc(self):
        for n in self.data:
            if n != Fraction(0):
                return n
        return Fraction(0)

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

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        n = self.deg()
        m = other.deg()
        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        degree = n + m
        p = [Fraction(0)] * degree
        for i in range(n):
            for j in range(m):
                if ap[i] != 0 and bp[j] != 0:
                    p[i + j] += ap[i] * bp[j]
        p.reverse()
        return Polynomial(p).trim()

    def __add__(self, other):
        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        while len(ap) < other.deg():
            ap.append(Fraction(0))
        for i in range(other.deg()):
            ap[i] += bp[i]
        ap.reverse()
        return Polynomial(ap)

    def __sub__(self, other):
        ap, bp = self.data.copy(), other.data.copy()
        ap.reverse(), bp.reverse()
        while len(ap) < other.deg():
            ap.append(Fraction(0))
        for i in range(other.deg()):
            ap[i] -= bp[i]
        ap.reverse()
        return Polynomial(ap).trim()

    def copy(self):
        return Polynomial(self.data)

    def __truediv__(self, other):
        q = [Fraction(0)] * (self.deg() + other.deg())
        r = self.copy()
        deg_r, deg_b = r.deg(), other.deg()
        while deg_r >= deg_b:
            lc_div = r.lc() / other.lc()
            q[deg_r - deg_b] += lc_div
            n = Polynomial(lc_div, deg_r - deg_b)
            nb = n * other
            r = r - nb
            deg_r = r.deg()
        q.reverse()
        return Polynomial(q).trim(), r

    def gcd(self, other):
        a = self.copy()
        b = other.copy()
        while b.deg() > 0:
            b, a = a - b, b
        return Polynomial(Fraction(1) / a.lc())

    def euclid(self, other):
        x, v, y, u = Polynomial(1), Polynomial(1), Polynomial(0), Polynomial(0)
        a, b = self.copy(), other.copy()
        while b.deg():
            q, r = a / b
            a = b
            b = r
            xp = x
            yp = y
            x = u
            y = v
            u = xp - q * u
            v = yp - q * v
        lca = Polynomial(Fraction(1) / a.lc())
        return x * lca, y * lca

    def euclidl(self, other):
        x, v, y, u = Polynomial(1), Polynomial(1), Polynomial(0), Polynomial(0)
        a, b, t, i = self.copy(), other.copy(), [], 1
        t.append([' '] * 10)
        t[0][0], t[0][1], t[0][4], t[0][5], t[0][6], t[0][7] = a, b, x, y, v, u
        while b.deg():
            q, r = a / b
            a = b
            b = r
            xp = x
            yp = y
            x = u
            y = v
            u = xp - q * u
            v = yp - q * v
            t.append([' '] * 10)
            t[i][0] = a
            t[i][1] = b
            t[i - 1][2] = q
            t[i - 1][3] = r
            t[i][4] = x
            t[i][5] = y
            t[i][6] = v
            t[i][7] = u
            t[i - 1][8] = xp
            t[i - 1][9] = yp
            i += 1
        lca = Polynomial(Fraction(1) / a.lc())
        for r in range(len(t)):
            for c in range(10):
                t[r][c] = strl(t[r][c])
        print('We use the Extended Euclidian Algorithm for Polynomials:\\\\')
        for r in range(len(t) - 1):
            print('\\polylongdiv{' + t[r][0] + '}{' + t[r][1] + '}\\\\')
            print('\\begin{itemize}')
            print('\\item $q\\leftarrow ' + t[r][2] + ',\\ r\\leftarrow ' + t[r][3] + '$\\\\')
            print('$a\\leftarrow ' + t[r + 1][0] + ',\\ b\\leftarrow ' + t[r + 1][1] + '$\\\\')
            print('$x\'\\leftarrow ' + t[r][8] + ',\\ y\'\\leftarrow ' + t[r][9] + '$\\\\')
            print('$x\\leftarrow ' + t[r + 1][4] + ',\\ y\\leftarrow ' + t[r + 1][5] + '$\\\\')
            print('$u\\leftarrow ' + t[r + 1][7] + ',\\ v\\leftarrow ' + t[r + 1][6] + '$\\\\')
            print('Verify: we have $x(' + t[0][0] + ') + y(' + t[0][1] + ') = a$ and $u(' + t[0][0] + ') + v(' +
                  t[0][1] + ')=b$')
            print('\\end{itemize}')
        print('We get the table:')
        print('\\begin{table}[h]\n\\begin{tabular}{r|r|r|r|r|r}')
        tb = '\\multicolumn{1}{c}{$' + '$} & \\multicolumn{1}{|c}{$'.join(['a', 'b', 'q', 'r', 'x', 'y', 'v', 'u',
                                                                           'x\'', 'y\''][:6]) + '$} '
        for r in range(len(t)):
            tb += '\\\\\\hline\\\n$' + '$ & $'.join(t[r][:6]) + '$'
        print(tb)
        print('\\end{tabular}\n\\end{table}\n\\begin{table}[h]\n\\begin{tabular}{r|r|r|r}')
        tb = '\\multicolumn{1}{c}{$' + '$} & \\multicolumn{1}{|c}{$'.join(['a', 'b', 'q', 'r', 'x', 'y', 'v', 'u',
                                                                           'x\'', 'y\''][6:]) + '$} '
        for r in range(len(t)):
            tb += '\\\\\\hline\n$' + '$ & $'.join(t[r][6:]) + '$'
        print(tb)
        print("\\end{tabular}\n\\end{table}")
        print('\\\\')
        print('So we get:\\\\')
        print('$u(x)(' + t[0][0] + ')+v(x)(' + t[0][1] + ')$')
        for r in range(len(t)):
            print('\\\\$=gcd(' + t[r][0] + ',' + t[r][1] + ')$')
        print('$\\\\=1$')
        print('\\\\\n\\\\Then taking $x = ' + strl(lca) + '(' + t[-1][4] + ')$ and $y= ' + strl(lca) + '(' +
              t[-1][5] + ')$,\n\\\\to finally get:\n\\\\\\[(' + t[-1][4] + ')(' + t[0][0] + ')+(' + t[-1][5] + ')('
              + t[0][1] + ')=1\\]\n\\\\')
        return x * lca, y * lca

    def __len__(self):
        return len(self.data)

    def trim(self):
        self.data = self.data[len(self.data) - self.deg():]
        if len(self.data) == 0:
            self.data = [Fraction(0)]
        return self

    def __mod__(self, other):
        if type(other) == Fraction:
            print('Fractions are not yet implemented for %')
        elif type(other) == int:
            a = self.data.copy()
            m = other
            for i in range(len(a)):
                while a[i] < 0:
                    a[i] += m
                while a[i] >= m:
                    a[i] -= m
            return Polynomial(a)
        raise TypeError('Type not compatible')

    def __lt__(self, other):
        return other > self

    def __le__(self, other):
        return other >= self

    def __gt__(self, other):
        s = self.copy()
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            return False
        elif deg_o < deg_s:
            return True
        s = s - other
        return s.lc() > 0

    def __ge__(self, other):
        s = self.copy()
        deg_s = s.deg()
        deg_o = other.deg()
        if deg_s < deg_o:
            return False
        elif deg_o < deg_s:
            return True
        s = s - other
        return s.lc() >= 0

    def __ne__(self, other):
        s = self.copy()
        s = s - other
        return s.deg() != 0 or s.lc() != 0

    def __eq__(self, other):
        s = self.copy()
        s = s - other
        return s.deg() == 0 and s.lc() == 0

    def pow(self, p: int):
        s = self.copy()
        e = s
        for i in range(p - 1):
            e *= s
        return e

    def shift_first_element(self, d):
        deg = self.deg()
        if d < deg:
            raise ValueError('d must be larger than current degree')
        self.data.reverse()
        for i in range(deg - d):
            self.data.append(Fraction(0))
        self.data[-1], self.data[deg] = self.data[deg], Fraction(0)
        self.data.reverse()

    def irreducible(self):
        q = 0 # ???????
        print('X^' + str(q) + ' - X')
        x = Polynomial('X^' + str(q) + ' - X')
        t = 1
        while self.gcd(x) == 1:
            x.shift_first_element(q)
            t += 1
        return t == q


def strl(self):
    if type(self) == Polynomial or type(self) == Fraction:
        return self.strl()
    return str(self)


def power_mod(x, n, m=float('Inf')):
    print('$x = ' + str(x) + ',\\ m = ' + str(m) + ',\\ z \\leftarrow 1$\\\\')
    z = 1

    while n > 1:
        print('$' + str(n) + ' > 1$,\\ ')
        if n % 2 == 1:
            print('$' + str(n) + '$ is uneven, so $z = z \\cdot x = ' + str(z) + '\\cdot' + str(x) + '=' + str(z*x) + '\\ (\\text{mod }' + str(m) + ') = ' + str(z * x % m) + '$, ')
            z = z * x % m
            print('$x = x \cdot x = ' + str(x) + '\cdot' + str(x) + '=' + str(x * x) + '\\ (\\text{mod }' + str(m) + ') = ' + str(x * x % m) + '$, $n = \\frac{' + str(n) + ' - 1}{2} = ' + str((n-1)//2) + '$\\\\')
            x = x * x % m
            n = (n-1)//2
        else:
            print('$' + str(n) + '$ is even, so $x = x \\cdot x = ' + str(x) + '\\cdot' + str(x) + '=' + str(x * x) + '\\ (\\text{mod }' + str(m) + ') = ' + str(x * x % m) + '$, $n = \\frac{' + str(n) + '}{2} = ' + str(n//2) + '$\\\\')
            x = x * x % m
            n //= 2
    print('$' + str(n) + ' \\not > 1$, so output $x\\cdot z = '+ str(x) + '\\cdot' + str(z) + ' = ' + str(x*z) + '\\ (\\text{mod }' + str(m) + ') = ' + str(x*z%m) + '$')
    return z * x % m


# print(poly([-1, 1, -1, 0, 1]))
# print(mul([-1, 1, -1, 0, 1], [3, 4, 5]))
# print(div([-1, 1, -1, 0, 1], [3, 4, 5]))
# print(deg([3, 4, 5]))
# print(mul([1,2,0], [1,1]))
# print(deg(mul([1,2,0], [1,1])))
# print(sub([1,1,1],[1,1,1]))
# print(n_x(0,3))
# print(n_x(2,3))
# print(div([1,2,0,-1,0,1],[1,0,0,0,-1]))
# print(div([1,1,1],[1,1]))
# print(add([1,1,1],[1,1,1,1,1,1]))
# print(euclid([1, 2, 0, -1, 0, 1], [1, 0, 0, 0, -1]))

# print(Fract(3, 9) / Fract(5, 9), Fract(0))

# print(Polynomial([Fract(1), Fract(2), Fract(3)], 100))

# print(Polynomial([1, 2, 3, 4, 5, 6]).euclid(Polynomial([1, 2, 3, 4, 5, 6])))
# print(Polynomial([1,2,0,-1,0,1])/Polynomial([1,0,0,0,-1]))
# print(Polynomial([1,2,0,-1,0,1])/Polynomial([3,4,5]))
# print(Polynomial([1,2,0,-1,0,1]).euclid(Polynomial([3,4,5])))
# print(Polynomial([1,2,0,-1,0,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,0,0]).euclid(Polynomial([3,4,5,9,9,0,0,0,0,9,9,9])))
# print(Polynomial([1, 2, 3, 4, 5, 6]) * Polynomial([1, 2, 3, 4, 5, 6]))
# print(Fract(0) + 0.1 > Fract(0, -6))
# print(Fract(0) - 2 + Fract(8, 700))
# print(Fract(0) - Fract(8, 700))
# print(Fract(8, 700) - 0)
# print(Fract(0) - 2)
# print(Polynomial([1,2,0,-1,0,1])/Polynomial([3,4,5]))
# test = Fract(13000, 2080008)
# test.reduce()
# print(test)

# print(Polynomial('X^3+2X^2+7X+1').euclidl(Polynomial('X^2+3X+1')))
# print(Polynomial('X^3+X+1').euclid(Polynomial('X^2+1'), True))
# print(Polynomial('X^3+X^2+2X+1').euclid(Polynomial('X^2+1'), True))
# print(Polynomial('X^2+1')-Polynomial('X^2+1'))
#
# print(Polynomial('X^3+X^2+2X+1'))
# print(Polynomial('X^3+X^2+5X+1') % 2)
# print(float(Fraction(600,33)))

# print(Polynomial('X^2+1') < Polynomial('X^2+1'))
# print(Polynomial('X^2+1') >= Polynomial('X^2+1'))
# print(Polynomial('X^2+1') == Polynomial('X^2+1'))
# print(Polynomial('X^2+1') != Polynomial('X^2+1'))
# print(Polynomial([0, 0, 0, 0, 0, 1]).lc())
# print(Polynomial([1, 2, 3]).pow(2))
# print(Polynomial([1,2,3,4]).irreducible())

# print(Polynomial('X^2+X+4') * Polynomial('X^2+X+4'))

print(power_mod(13, 280, 561))
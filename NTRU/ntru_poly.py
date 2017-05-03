# Class containing implementation of a polynomial used for NTRU
class NTRUPoly(object):

    def __init__(self, coeff=[]):
        """Representing each polynomial as a list of coefficients

        Example: [1, 2, 3] represents 1 + 2x + 3x^2
        """
        self._coeff = coeff

    def _fluff(self, poly_coeff):
        # Add leading 0's so that self is the same size as poly
        if len(poly_coeff) > len(self._coeff):
            self._coeff = self._coeff + [0]*(len(poly_coeff) - len(self._coeff))

    def trim(self):
        # Remove all leading 0's
        while self._coeff[-1] == 0 and len(self._coeff) > 1:
            del self._coeff[-1]

    def degree(self):
        self.trim()
        return len(self._coeff)

    def __add__(self, poly):
        # Sums two polynomials
        self._fluff(poly._coeff)
        poly._fluff(self._coeff)

        new_coeff = [0]*len(self._coeff)
        for i in range(len(self._coeff)):
            new_coeff[i] = self._coeff[i] + poly._coeff[i]
        self.trim()
        poly.trim()
        new_poly = self.__class__(new_coeff)
        new_poly.trim()
        return new_poly

    def __sub__(self, poly):
        # Subtracts poly from self
        self._fluff(poly._coeff)
        poly._fluff(self._coeff)

        new_coeff = [-1*i for i in poly._coeff]
        neg_poly = self.__class__(new_coeff)
        return self.__add__(neg_poly)

    def mod(self, q):
        # Reduces coefficients of the polynomial mod q
        for i in range(len(self._coeff)):
            self._coeff[i] = self._coeff[i] % q
        self.trim()

    def mod_center(self, q):
        # Reduces coefficients of the polynomial mod q
        # But bounds the absolute value of the coefficients by q/2
        u_bound = float(q) / 2
        l_bound = -1*float(q) / 2
        self.mod(q)
        for i in range(len(self._coeff)):
            if self._coeff[i] > u_bound:
                self._coeff[i] = self._coeff[i] % -q
            elif self._coeff[i] < l_bound:
                self._coeff[i] = self._coeff[i] % q

    def __mul__(self, poly):
        # Multiplies two polynomials
        prod_order = (len(self._coeff)-1) + (len(poly._coeff)-1)
        prod_coeff = [0]*(prod_order+1)
        for i in range(len(self._coeff)):
            for j in range(len(poly._coeff)):
                prod_coeff[j+i] = prod_coeff[j+i] + self._coeff[i]*poly._coeff[j]
        prod = self.__class__(prod_coeff)
        prod.trim()
        return prod

    def div(self, divisor):
        # Divides this instance of NTRUPoly by divisor
        # Returns a quotient and a remainder (both NTRUPoly instances)
        N = NTRUPoly(self._coeff)
        D = NTRUPoly(divisor._coeff)
        q = NTRUPoly([0]*N.degree())

        if N.degree() >= D.degree():
            while N.degree() >= D.degree() and N.degree() > 1:
                shift = N.degree() - D.degree()
                d = NTRUPoly([0]*shift + D._coeff)
                new_q_coeff = q._coeff + [0]*N.degree()
                new_q_coeff[shift] = new_q_coeff[shift] + (N._coeff[-1] / float(d._coeff[-1]))
                q = NTRUPoly(new_q_coeff)
                d = d * NTRUPoly([new_q_coeff[shift]])
                N = N - d
            r = N
            q.trim()
            return [q, r]

        else:
            return [NTRUPoly([0]), N]

    def extended_euclid(self, poly):
        # Copies of both polynomials
        if len(self._coeff) >= len(poly._coeff):
            a = self.__class__(self._coeff)
            b = self.__class__(poly._coeff)
        else:
            a = self.__class__(poly._coeff)
            b = self.__class__(self._coeff)

        x_0 = self.__class__([1])
        x_1 = self.__class__([0])
        y_0 = self.__class__([0])
        y_1 = self.__class__([1])

        iters = 0
        while b._coeff != [0]:
            q, r = a.div(b)
            a = b
            b = r
            print "a: " + str(a._coeff)
            print "b: " + str(b._coeff)
            x_0, x_1 = x_1, x_0 - (q*x_1)
            y_0, y_1 = y_1, y_0 - (q*y_1)

            iters = iters+1
            if iters == 1000:
                break

        # Flip x,y if we swapped inputs
        if len(self._coeff) <  len(poly._coeff):
            x_0, y_0 = y_0, x_0

        # Normalize so that the leading term is 1
        scale = a._coeff[-1]
        inv_scale = NTRUPoly([float(1/scale)])
        a = a * inv_scale
        x_0 = x_0 * inv_scale
        y_0 = y_0 * inv_scale

        return [a, x_0, y_0]


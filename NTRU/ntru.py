import math
from ntru_poly import NTRUPoly

# An instance of NTRU, not for real use
# Initialize with parameters, provides encrypt and decrypt
class NTRU:

    def __init__(self, N, p, q, f, g):
        self.N = N # polynomial size
        self.p = p # small prime
        self.q = q # big prime (way bigger than 2p)

        # note, gcd(f,g) must be 1
        # both polynomials should be size N at most
        self.f = f # NTRUPoly w/ coefficients 1,0,-1
        self.g = g # NTRUPoly w/ coefficients 1,0,-1

        self.verify_parameters()

        self.f_p = self.compute_inverse(self.f, self.p)
        self.f_q = self.compute_inverse(self.f, self.q)

        self.verify_inverses()

        self.h = (self.f_q * self.g)
        self.h.mod(self.q) 

    def verify_parameters(self):
        # Check that p,q,f,g have the right properties
        if not (self.is_prime(self.p)):
            raise Exception("Parameter p is not prime.")
        if not (self.is_prime(self.q)):
            raise Exception("Parameter q is not prime.")
        gcd, s, t = self.f.extended_euclid(self.g)
        if gcd._coeff != [1]:
            raise Exception("Parameters f and g are not relatively prime.")

    def verify_inverses(self):
        # Check that f_p and f_q are indeed inverses
        # of f with respect to p and q
        prod1 = self.f_p * self.f
        prod1.mod(self.p)
        if not ([1] == prod1._coeff):
            raise Exception("f_p and f are not inverses mod p.")
        prod2 = self.f_q * self.f
        prod2.mod(self.q)
        if not ([1] == prod2._coeff):
            raise Exception("f_q and f are not inverses mod q.")

    def compute_inverse(self, poly, n):
        # Computes the inverse of the polynomial when
        # the coefficients are taken mod n
        d = NTRUPoly([-1] + [0]*(self.N - 1) + [1])
        gcd, s, t = poly.extended_euclid(d)
        s.mod(n)
        print "s: " + str(s._coeff)
        print "t: " + str(t._coeff)
        return s

    def is_prime(self, n):
        if n % 2 == 0 or n < 2:
            return False
        else:
            for i in range(3, int(math.sqrt(n))+1):
                if n % i == 0:
                    return False
        return True

    def encrypt(self, m, rand_poly):
        # Encrypts message m using self.h and a random polynomial
        # From paper: e = (p*(rand) * h) + m mod q
        # In practice we need to use d to keep e in the ring space
        p_poly = NTRUPoly([self.p])
        e_prime = ((p_poly*rand_poly)*self.h) + m
        d = NTRUPoly([-1] + [0]*(self.N - 1) + [1])
        quot, r = e_prime.div(d)
        r.mod(self.q)
        return r

    def decrypt(self, e):
        # Decrypts message e using self.f and self.f_p
        # From paper: m = f_p * (f * e mod q) mod p
        # In practice we need to use d to keep products in ring space
        d = NTRUPoly([-1] + [0]*(self.N - 1) + [1])
        prod1 = self.f * e
        quot, r = prod1.div(d)
        r.mod_center(self.q)
        prod2 = self.f_p * r
        quot, r = prod2.div(d)
        r.mod(self.p)
        r.trim()
        return r

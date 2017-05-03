import math
from ntru_poly import NTRUPoly

# An instance of NTRU, not for real use
# Initialize with parameters, provides encrypt and decrypt
class NTRU:

    def __init__(N, p, q, f, g):
        self.N = N # polynomial size
        self.p = p # small prime
        self.q = q # big prime (way bigger than 2p)

        # note, gcd(f,g) must be 1
        # both polynomials should be size N at most
        self.f = f # NTRUPoly w/ coefficients 1,0,-1
        self.g = g # NTRUPoly w/ coefficients 1,0,-1

        self.verify_parameters()

        self.f_p = self.compute_inverse(f, p)
        self.f_q = self.compute_inverse(f, q)
        self.h = (self.f_q * self.g).mod(self.q) 

    def verify_parameters(self):
        if not (self.is_prime(self.p)):
            raise Exception("Parameter p is not prime.")
        if not (self.is_prime(self.q)):
            raise Exception("Parameter q is not prime.")
        gcd, s, t = self.f.extended_euclid(self.g)
        if gcd._coeff != [1]:
            raise Exception("Parameters f and g are not relatively prime.")

    def compute_inverse(poly, n):
        # Computes the inverse of the polynomial when
        # the coefficients are taken mod n
        # TODO: implement this
        return poly

    def is_prime(self, n):
        if n % 2 == 0 or n < 2:
            return False
        else:
            for i in range(3, int(math.sqrt(n))+1):
                if n % i == 0:
                    return False
        return True

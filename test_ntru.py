from NTRU.ntru import NTRU
from NTRU.ntru_poly import NTRUPoly


# Test script to demonstrate the NTRU class
if __name__ == "__main__":

    # Instantiate an NTRU instance
    # N = 8, p = 13, q = 9949
    # f,g are randomly selected ternary polynomials
    f = NTRUPoly([1,1,-1,0,-1,1])
    g = NTRUPoly([-1,0,1,1,0,0,-1])
    ntru = NTRU(7, 29, 491531, f, g)

    # Try a simple encryption and decryption
    print "Encrypting the number 5..."
    print "Generating a random polynomial for encryption..."
    rand = NTRUPoly([-1, 1, -1, 1])
    e = ntru.encrypt(NTRUPoly([5]), rand)
    print "Encrypted, 5 is: " + str(e._coeff)
    m = ntru.decrypt(e)
    print "Decryption yields: " + str(m._coeff)

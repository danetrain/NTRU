# Test script to verify that the NTRUPoly class works

from NTRU.ntru_poly import NTRUPoly

if __name__ == "__main__":
    # Tests trim method
    p1 = NTRUPoly([1, 0, 0, 0, 0, 0])
    p1.trim()
    assert [1] == p1._coeff

    p1 = NTRUPoly([0, 0, 0, 1])
    p1.trim()
    assert [0, 0, 0, 1] == p1._coeff

    # Tests addition, subtraction
    p1 = NTRUPoly([1, 2, 3, 4, 5])
    p2 = NTRUPoly([12, 0, 1])

    p3 = p1 + p2
    assert [13, 2, 4, 4, 5] == p3._coeff

    p4 = p3 - p1
    assert p2._coeff == p4._coeff

    # Tests multiplication
    p1 = NTRUPoly([-1, 1])
    p2 = NTRUPoly([1, 1])
    p3 = p1 * p2
    assert [-1, 0, 1] == p3._coeff

    p1 = NTRUPoly([3, 0, 4])
    p2 = NTRUPoly([-2, 1])
    p3 = p1 * p2
    p4 = p2 * p1
    assert p3._coeff == p4._coeff
    assert p3._coeff == [-6, 3, -8, 4]

    # Tests mod and mod_center
    p1 = NTRUPoly([50, 25, 40, 33, 24])
    p1.mod(12)
    assert [2, 1, 4, 9] == p1._coeff

    p1 = NTRUPoly([35, 33, 12, 170, 13])
    p1.mod_center(17)
    assert [1, -1, -5, 0, -4] == p1._coeff

    # Tests div
    p1 = NTRUPoly([-1, 0, 1])
    d = NTRUPoly([-1, 1])
    q, r = p1.div(d)
    assert [1, 1] == q._coeff
    assert [0] == r._coeff

    p1 = NTRUPoly([-4, 0, -2, 1])
    d = NTRUPoly([-3, 1])
    q, r = p1.div(d)
    assert [3, 1, 1] == q._coeff
    assert [5] == r._coeff

    p1 = NTRUPoly([3, 2, 1])
    p2 = NTRUPoly([2, 1])
    q, r = p1.div(p2)
    assert [0, 1] == q._coeff
    assert [3] == r._coeff

    p1 = NTRUPoly([5, 1])
    p2 = NTRUPoly([14])
    q, r = p1.div(p2)

    # Tests polynomial extended euclidean
    p1 = NTRUPoly([-1, 0, 1])
    p2 = NTRUPoly([1, -2, 1])
    gcd, s, t = p1.extended_euclid(p2)
    assert [-1, 1] == gcd._coeff

    p2 = NTRUPoly([-3, 2, 1])
    gcd, s, t = p1.extended_euclid(p2)
    assert [-1, 1] == gcd._coeff

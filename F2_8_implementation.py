
#base_polynomial = ["x^8", "x^4", "x^3", "x", "1"] #the AES polynomial

irreducible_polynomial = int("100011011", 2)
p = 253
q = 113

field_characteristic = 2
field_degree = 8


#thanks to Nikolay S. Kaleyski for C code, and thanks to chatgpt for translation to python
def multiply(p, q, primal_poly, degree):
    result = 0
    # The value at which we should reduce using the irreducible polynomial
    cutoff = 1
    for i in range(degree-1):
        cutoff <<= 1
    while p and q:
        if q & 1: # If b is odd, add a to the total
            result ^= p
        if p & cutoff:
            p = (p << 1) ^ primal_poly # reduce
        else:
            p <<= 1
        q >>= 1
    return result


def add(p, q):
    return p^q


'''
'''
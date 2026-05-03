from math import gcd

def RSA(p, q, message):
    n = p * q
    t = (p - 1) * (q - 1)

    for e in range(2, t):
        if gcd(e, t) == 1:
            break

    d = pow(e, -1, t)

    ct = pow(message, e, n)
    print("Encrypted message is", ct)

    mes = pow(ct, d, n)
    print("Decrypted message is", mes)


RSA(3, 7, 9)
RSA(3, 7, 17)
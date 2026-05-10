import numpy as np

keyMatrix = [[0]*3 for _ in range(3)]
messageVector = [[0] for _ in range(3)]
cipherMatrix = [[0] for _ in range(3)]


def getKeyMatrix(key):
    k = 0
    for i in range(3):
        for j in range(3):
            keyMatrix[i][j] = ord(key[k]) - 65
            k += 1


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x


def matrix_inverse(A):

    det = round(np.linalg.det(A))
    det_mod = det % 26
    det_inv = mod_inverse(det_mod, 26)
    adj = np.linalg.inv(A) * det
    adj = np.round(adj).astype(int)

    return (det_inv * adj) % 26


def encrypt():

    for i in range(3):
        cipherMatrix[i][0] = 0
        for j in range(3):
            cipherMatrix[i][0] += keyMatrix[i][j] * messageVector[j][0]

        cipherMatrix[i][0] %= 26


def decrypt():

    A_inv = matrix_inverse(np.array(keyMatrix))

    print("\nInverse Key Matrix:")
    print(A_inv)

    decrypted = [[0] for _ in range(3)]

    for i in range(3):

        for x in range(3):
            decrypted[i][0] += A_inv[i][x] * cipherMatrix[x][0]

        decrypted[i][0] %= 26

    return decrypted


def HillCipher(message, key):

    getKeyMatrix(key)

    print("Key Matrix:")
    for row in keyMatrix:
        print(row)

    for i in range(3):
        messageVector[i][0] = ord(message[i]) - 65

    print("\nMessage Matrix:")
    for row in messageVector:
        print(row)

    encrypt()

    print("\nCipher Matrix:")
    for row in cipherMatrix:
        print(row)

    print("\nEncrypted Text:", end=" ")

    for i in cipherMatrix:
        print(chr(i[0] + 65), end="")

    decrypted = decrypt()

    print("\nDecrypted Matrix:")
    for row in decrypted:
        print(row)

    print("\nDecrypted Text:", end=" ")

    for i in decrypted:
        print(chr(int(i[0]) + 65), end="")


HillCipher("MOR", "RVCRSCFVT")

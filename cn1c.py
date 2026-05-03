import numpy as np

# Global matrices
keyMatrix = [[0]*3 for _ in range(3)]
messageVector = [[0] for _ in range(3)]
cipherMatrix = [[0] for _ in range(3)]


# Convert key string to 3x3 matrix
def getKeyMatrix(key):
    k = 0
    for i in range(3):
        for j in range(3):
            keyMatrix[i][j] = ord(key[k]) - 65
            k += 1


# Find modular inverse
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Modular inverse does not exist")


# Determinant of 3x3 matrix
def determinant(matrix):
    a,b,c,d,e,f,g,h,i = matrix.flatten()
    return (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g))


# Adjugate of matrix
def adjugate(matrix):
    a,b,c,d,e,f,g,h,i = matrix.flatten()

    adj = np.array([
        [ (e*i - f*h), -(b*i - c*h),  (b*f - c*e)],
        [-(d*i - f*g),  (a*i - c*g), -(a*f - c*d)],
        [ (d*h - e*g), -(a*h - b*g),  (a*e - b*d)]
    ])

    return adj.T


# Matrix inverse mod 26
def matrix_inverse(A, mod=26):

    det = determinant(A) % mod
    det_inv = mod_inverse(det, mod)

    adj = adjugate(A)

    inv = (det_inv * adj) % mod

    return inv


# Encryption
def encrypt(messageVector):

    for i in range(3):
        cipherMatrix[i][0] = 0

        for j in range(3):
            cipherMatrix[i][0] += keyMatrix[i][j] * messageVector[j][0]

        cipherMatrix[i][0] %= 26


# Decryption
def decrypt(cipherMatrix, keyMatrix):

    A = np.array(keyMatrix)
    A_inv = matrix_inverse(A)

    print("\nInverse Key Matrix (mod 26):")
    print(A_inv)

    decryptedMatrix = [[0] for _ in range(3)]

    for i in range(3):
        for j in range(1):

            decryptedMatrix[i][j] = 0

            for x in range(3):
                decryptedMatrix[i][j] += A_inv[i][x] * cipherMatrix[x][j]

            decryptedMatrix[i][j] %= 26

    return decryptedMatrix


# Hill Cipher Function
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

    encrypt(messageVector)

    print("\nCipher Matrix:")
    for row in cipherMatrix:
        print(row)

    CipherText = ""
    for i in range(3):
        CipherText += chr(cipherMatrix[i][0] + 65)

    print("\nCiphertext:", CipherText)

    decryptedMatrix = decrypt(cipherMatrix, keyMatrix)

    print("\nDecrypted Matrix:")
    for row in decryptedMatrix:
        print(row)

    DecryptedText = ""
    for i in range(3):
        DecryptedText += chr(decryptedMatrix[i][0] + 65)

    print("\nDecrypted Text:", DecryptedText)


# Driver Code
def main():

    message = "MOR"
    key = "RVCRSCFVT"

    HillCipher(message, key)


if __name__ == "__main__":
    main()
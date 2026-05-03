import string
import random

def generate_substitution_key():
    alphabet = list(string.ascii_lowercase)
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))


def encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            new_char = key[char.lower()]
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result


def decrypt(text, key):
    reverse_key = {v: k for k, v in key.items()}
    result = ""
    for char in text:
        if char.isalpha():
            new_char = reverse_key[char.lower()]
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result


substitution_key = generate_substitution_key()
print("Substitution Key:", substitution_key)

plaintext = input("Enter the plain text: ")

ciphertext = encrypt(plaintext, substitution_key)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)

decrypted_text = decrypt(ciphertext, substitution_key)
print("Decrypted Text:", decrypted_text)
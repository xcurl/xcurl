def caesar_cipher(text, shift):
    result = ""
    shift = shift % 26

    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char

    return result


plaintext = input("Enter the plain text: ")
shift = int(input("Enter the number of shifts: "))

ciphertext = caesar_cipher(plaintext, shift)
originaltext = caesar_cipher(ciphertext, -shift)

print("Plaintext for caesar:", plaintext)
print("Shift:", shift)
print("Ciphertext from caesar:", ciphertext)
print("Originaltext for caesar:", originaltext)
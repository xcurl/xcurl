import hashlib

def compute_hash(text, algo):
    data = text.encode()

    if algo == "SHA-1":
        h = hashlib.sha1()
    else:
        h = hashlib.sha512()

    h.update(data)
    return h.hexdigest()


text = input("Enter text: ")
algo = input("Enter algorithm (SHA-1 / SHA-512): ")

if text:
    result = compute_hash(text, algo)
    print("Hash:", result)
else:
    print("Please enter a valid input string.")
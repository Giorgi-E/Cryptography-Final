from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib

# Bob generates the RSA keys
def generate_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open("private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        ))

    with open("public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key

# Then we encrypt the file using AES
def encrypt_file(public_key):
    # Alice creates a plaintext message:
    plaintext = b"Hello Bobby."
    with open("alice_message.txt", "wb") as f:
        f.write(plaintext)

    # Alice generates a random AES-256 key and IV
    aes_key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)       # 128-bit IV

    # Encrypting the file using AES-256 with the generated key and IV
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open("encrypted_file.bin", "wb") as f:
        f.write(iv + ciphertext)

    # Encrypt the AES key using Bob’s RSA public key
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("aes_key_encrypted.bin", "wb") as f:
        f.write(encrypted_key)
    original_hash = hashlib.sha256(plaintext).hexdigest()
    with open("original_hash.txt", "w") as f:
        f.write(original_hash)

# Decryting the file using RSA and AES
def decrypt_file(private_key):
    with open("aes_key_encrypted.bin", "rb") as f:
        encrypted_key = f.read()
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open("encrypted_file.bin", "rb") as f:
        data = f.read()
    iv = data[:16]
    ciphertext = data[16:]

    # Bob uses the decrypted AES key and IV to decrypt the file
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    with open("decrypted_message.txt", "wb") as f:
        f.write(decrypted)

    # Now we can compute the SHA-256 hash of the file and compare it to the original hash for integrity verification
    with open("original_hash.txt", "r") as f:
        original_hash = f.read()
    new_hash = hashlib.sha256(decrypted).hexdigest()
    print("\n Integrity verified" if new_hash == original_hash else "\n Integrity verification failed!")

if __name__ == "__main__":
    private_key, public_key = generate_rsa_keys()
    encrypt_file(public_key)
    decrypt_file(private_key)

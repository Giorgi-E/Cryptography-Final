from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

#We first generate the RSA key pair
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open("private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key

#Then using the public key we encrypt the file
def encrypt(public_key):
    message = b"Saidumlo Shetyobineba"
    with open("message.txt", "wb") as f:
        f.write(message)

    aes_key = Fernet.generate_key()
    fernet = Fernet(aes_key)
    encrypted_message = fernet.encrypt(message)

    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("aes_key_encrypted.bin", "wb") as f:
        f.write(encrypted_key)
    with open("encrypted_message.bin", "wb") as f:
        f.write(encrypted_message)

#Now we can decrypt with the private key
def decrypt(private_key):
    with open("aes_key_encrypted.bin", "rb") as f:
        encrypted_key = f.read()

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("encrypted_message.bin", "rb") as f:
        encrypted_message = f.read()

    fernet = Fernet(aes_key)
    decrypted_message = fernet.decrypt(encrypted_message)

    with open("decrypted_message.txt", "wb") as f:
        f.write(decrypted_message)

if __name__ == "__main__":
    private_key, public_key = generate_keys()
    encrypt(public_key)
    decrypt(private_key)

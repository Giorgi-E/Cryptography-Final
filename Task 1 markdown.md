# Encrypted Messaging App Prototype

### Final exam task 1

This code implements a secure messaging system using both asymmetric and symmetric encryption mechanisms. Messages are encrypted with AES, and the AES key itself is encrypted using RSA so that only the recipient on the other side can decrypt it.

##### 1. RSA Key Generation (User A)
- **User A** generates a 2048-bit RSA key pair.
- The **private key** is securely saved in `private.pem` file.
- The **public key** is saved in `public.pem` file and is later shared with **User B**.

##### 2. Message Encryption (User B)
- **User B** generates the message text.
- Then **symmetric AES key** is generated. For this I used Python’s *Fernet* module from the cryptography library.
- The message is then enrypted using this **AES key**.
- The resulting ciphertext is written out to `encrypted_message.bin`.
-  The resulting AES key is encrypted with **RSA** using User A’s **public key**.
-  Finally this newly RSA-encrypted AES key is saved as `aes_key_encrypted.bin`

##### 3. Message Decryption (User A)
- User A get their **private RSA key** from `private.pem`.
- User A then decrypts `aes_key_encrypted.bin` file using RSA key, getting the original **AES** key that was used for message encryption.
- This **AES** key is used to decrypt the message - `encrypted_message.bin` file.
- Finally we get the original message in plaintext and save it to  `decrypted_message.txt` file.

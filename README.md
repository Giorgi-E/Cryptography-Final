Secure File Exchange Using RSA + AES

##Encryption Flow

### 1. Key Generation (Bob)
- Using Python code we generate an RSA key pair for Bob.
- This private key is stored in `private.pem`.
- The public key is stored in `public.pem` and shared with Alice.

### 2. Message Creation (Alice)
- Alice creates a plaintext message in a file called alice_message.txt.
- I do this straight inside the python codebase.

### 3. AES Key + IV Generation
- Alice generates a random 256-bit AES key (`aes_key`) and a 128-bit IV (`iv`).

### 4. File Encryption
- Next we encrypts `alice_message.txt` using AES-256.
- The output is saved in `encrypted_file.bin` file.

### 5. AES Key Encryption (RSA)
- Alice encrypts the AES key using Bob’s RSA public key.
- This resuling encrypted AES key is saved in `aes_key_encrypted.bin`.

### 6. AES Key Decryption (Bob)
- Now the decryption starts.
- Bob decrypts `aes_key_encrypted.bin` using his RSA private key, with the result being the original AES key.

### 7. File Decryption
- We then extract the IV and ciphertext from `encrypted_file.bin`.
- Bob decrypts it using the AES key + IV to get the original message.
- Output in plaintext form is written to `decrypted_message.txt`.

### 8. Integrity Verification
- Finally we verify the integrity of the files.
- Alice also sends a SHA-256 hash of the original file.
- Bob computes a SHA-256 hash of `decrypted_message.txt` and compares it.
- If the hashes match, the file is unmodified and integrity verified.


## RSA vs AES

AES is a symmetric encryption algorithm that is uses one key for encryption and decryption. 
It is very fast and ideal for large amounts of data.
RSA is an asymmtric encryption algorithm that uses a pair of keys - public and private.
RSA is slower than AES and used for secure key exchanges and digital signatures.
AES is preferred for speed and efficiency, while RSA is essential for secure key distribution in hybrid encryption systems.
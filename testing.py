from AES_encryption import encrypt
from AES_decryption import decrypt
from utils import string_to_binary, binary_to_string, unlim_bin_to_hex, secret_to_binary

secret = "lolEncryptionKey"

if __name__ == "__main__":
    plaintext = "abcdefghijklmnopqrstuvwxyzæøå" 
    plaintext_binary = string_to_binary(plaintext)
    key_binary = secret_to_binary(secret)
    ciphertext = encrypt(plaintext_binary, key_binary)
    print(f"Plaintext:        {plaintext_binary}")
    print(f"After decryption: {decrypt(ciphertext, key_binary)}")
    plaintext_after = decrypt(ciphertext, key_binary)
    #print(ciphertext)
    print(binary_to_string(plaintext_after))
    ciphertext_ascii = binary_to_string(ciphertext)
    print(ciphertext_ascii)



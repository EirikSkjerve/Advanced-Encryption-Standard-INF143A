from AES_encryption import encrypt, shift_rows
from generate_round_keys import generate_round_keys
from utils import string_to_binary, binary_to_string, unlim_bin_to_hex, secret_to_binary

secret = "aesEncryptionKey"

if __name__ == "__main__":
    plaintext = "Periphery in flames, deadmau5, and a bunch of stuff" 
    plaintext_binary = string_to_binary(plaintext)
    key_binary = secret_to_binary(secret)
    ciphertext = encrypt(plaintext_binary, key_binary)
    ciphertext_ascii = binary_to_string(ciphertext)
    ciphertext_hex = unlim_bin_to_hex(ciphertext)
    #print(ciphertext)
    print(ciphertext_ascii)
    print(ciphertext_hex)



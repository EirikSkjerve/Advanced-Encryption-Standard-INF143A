from AES_encryption import encrypt, shift_rows
from generate_round_keys import generate_round_keys
from utils import string_to_binary, binary_to_string

key = "10011110011111001111101100001010110000010100001011110100101011011001110011001001010010110100000001111011101010101010000101011011"
#plaintext = "0110010010110101001000100001010111000001101011101111001100011000111000011110001101011010000101110111110111110100111111000010101110000010010101000100010010000001000001111011001011110000001001000110111011101110011011010110101110100001001100110011110100100000"

#first round, not everything is implemented
if __name__ == "__main__":
    plaintext = "Hei dette er en test for å sjekke AES encryption cipher, some random characters =)(#!# ()S=DF =)U#R W=)DF" 
    plaintext_binary = string_to_binary(plaintext)
    ciphertext = encrypt(plaintext_binary, key)
    print(binary_to_string(ciphertext))



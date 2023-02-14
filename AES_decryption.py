from generate_round_keys import generate_round_keys
from utils import *
from F2_8_implementation import *

def decrypt(ciphertext, key):
    
    #splits up the ciphertext in 128-bit blocks
    blocks = split_blocks(ciphertext, 128)
    #generates the round keys
    round_keys = generate_round_keys(key)
    round_keys.reverse()
    
    #where plaintext will be placed
    plain_blocks = []
    
    #decrypts each 128-bit block separately
    for block in blocks:
        
        #perform 10 steps of diffusion and confusion
        for i in range(10):
            round_key = round_keys[i]
            block = decryption_round(block, round_key, i)
        block = (XOR(block, key))
        plain_blocks.append(block)
            
    return "".join(plain_blocks)
    
def decryption_round(cipher_block, round_key, round_number):
    
    #key addition
    cipher_block = XOR(cipher_block, round_key)
    
    blocks = split_blocks(cipher_block, 8)
    matrix = block_to_matrix(blocks)
    
    #mixcolumn inverse
    if round_number != 0:
        matrix = inv_mix_columns(matrix)

    #shiftrows inverse
    matrix = inv_shift_rows(matrix)
    
    main_blocks = split_blocks(matrix_to_block(matrix), 8)
    permuted_blocks = []
    # byte substitution inverse
    for b in main_blocks:
        permuted_blocks.append(s_box_get_inv(b))
    
    return "".join([x for x in permuted_blocks])


def inv_mix_columns(matrix):
    
    #inverse fixed matrix
    inv_A = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
    
    product_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    
    #performs ordinary matrix multiplication
    for i in range(4):
        for j in range(4):
            #the row of the fixed matrix
            A_row = inv_A[i]
            #converts from hex and extracts the column of the input matrix
            input_column = [int(matrix[x][j],16) for x in range(4)]
            
            #finite field multiplication and addition according to matrix multiplication
            product_matrix[i][j] = field_sum_list([multiply(A_row[x],input_column[x]) for x in range(4)])
    
    return integer_matrix_to_hex(product_matrix)

def inv_shift_rows(matrix):
    
    #inversely shifts the rows according to the AES standard
    matrix[1] = shift_right(matrix[1],1)
    matrix[2] = shift_right(matrix[2],2)
    matrix[3] = shift_right(matrix[3],3)
    
    return matrix

def shift_right(row, num_shifts):
    #performs a right shift num_shifts times
    temp = ["", "", "", ""]
    for r in range(len(row)):
        temp[(r+num_shifts)%4] = row[r]
    return temp


def integer_matrix_to_hex(int_matrix):
    converted_matrix = [["","","",""],["","","",""],["","","",""],["","","",""]]
    for i in range(4):
        for j in range(4):
            converted_matrix[i][j] = binary_to_hex(bin(int_matrix[i][j])[2:].zfill(8))
    return converted_matrix
from utils import split_blocks, XOR, s_box_get, binary_to_hex, hex_to_binary
from generate_round_keys import generate_round_keys
from F2_8_implementation import multiply, field_sum_list


def encrypt(plaintext, key)->str:
    
    #splits up the plaintext in 128-bit blocks
    blocks = split_blocks(plaintext, 128)
    
    #generates the round keys
    round_keys = generate_round_keys(key)
    
    #where ciphertext will be placed
    cipher_blocks = []
    
    #encrypts each 128-bit block separately
    for block in blocks:
        
        #step 1: xor the plaintext block with the main key
        block = XOR(block, key)
        
        #perform 10 steps of diffusion and confusion
        for i in range(10):
            round_key = round_keys[i+1]
            block = encryption_round(block, round_key, i)
            
        cipher_blocks.append(block)
            
    return "".join(cipher_blocks)

def encryption_round(plain_block, round_key, round_number):
    #split blocks into 16 bytes(8-bit strings)
    blocks = split_blocks(plain_block, 8)
    
    permuted_blocks = []
    
    #permutes all bytes according to the AES (8,8) function
    for block in blocks:
        block = (s_box_get(block))
        permuted_blocks.append(block)
    
    #performs the "shift rows" operation on the matrix constructed from the 16 bytes
    matrix = shift_rows(block_to_matrix(permuted_blocks))
    
    #performs the "mix columns" operation on the matrix on all but the last iteration of confusion/diffusion
    if round_number != 9:
        matrix = mix_columns(matrix)
    
    #converts the matrix back to a block of binary bits
    main_block = matrix_to_block(matrix)
    
    #performs an xor operation on the 128-bit block with the round key
    main_block = XOR(main_block, round_key)
    
    return main_block

def block_to_matrix(blocks):
    
    #converts every 8-bit sequence into hexadecimal
    hex_blocks = [binary_to_hex(b) for b in blocks]
    
    matrix = [["","","",""],
              ["","","",""],
              ["","","",""],
              ["","","",""]]
    
    #distributes the list of hex-values into the 4x4 matrix
    for h in range(16):
        row = h%4
        column = h//4
        matrix[row][column] = hex_blocks[h]
        
    return matrix

def matrix_to_block(matrix):
    #flattens the matrix into a list
    #takes in a matrix of integers, and converts them to binary
    #this method is apparently not efficient in terms of space time complexity
    main_block = [hex_to_binary(h) for h in sum(matrix, [])]
    main_block = "".join(main_block)
    return main_block

def shift_rows(matrix):
    
    #shifts the rows according to the AES standard
    matrix[1] = shift_left(matrix[1],1)
    matrix[2] = shift_left(matrix[2],2)
    matrix[3] = shift_left(matrix[3],3)
    
    return matrix

def shift_left(row, num_shifts):
    
    #performs a left shift num_shifts times
    temp = ["", "", "", ""]
    for r in range(len(row)):
        temp[(r-num_shifts)%4] = row[r]
    return temp

'''Have confirmed that this works as it should'''
def mix_columns(matrix):
    #fixed matrix A
    A = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
    #empty initialized product matrix
    product_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    
    #performs ordinary matrix multiplication
    for i in range(4):
        for j in range(4):
            #the row of the fixed matrix
            A_row = A[i]
            #converts from hex and extracts the column of the input matrix
            input_column = [int(matrix[x][j],16) for x in range(4)]
            
            #finite field multiplication and addition according to matrix multiplication
            product_matrix[i][j] = field_sum_list([multiply(A_row[x],input_column[x]) for x in range(4)])
    
    
    return integer_matrix_to_hex(product_matrix)



def integer_matrix_to_hex(int_matrix):
    converted_matrix = [["","","",""],["","","",""],["","","",""],["","","",""]]
    for i in range(4):
        for j in range(4):
            converted_matrix[i][j] = binary_to_hex(bin(int_matrix[i][j])[2:].zfill(8))
    return converted_matrix



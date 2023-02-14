from utils import split_blocks, XOR, s_box_get, binary_to_hex, hex_to_binary
from generate_round_keys import generate_round_keys
from F2_8_implementation import multiply, field_sum_list


def encrypt(plaintext, key)->str:
    
    blocks = split_blocks(plaintext, 128)
    round_keys = generate_round_keys(key)
    
    cipher_blocks = []
    
    for block in blocks:
        block = XOR(block, key)
        
        for i in range(10):
            round_key = round_keys[i+1]
            block = encryption_round(block, round_key, i)
            #print(f"Block after {i} iterations: {block}")
            
        cipher_blocks.append(block)
            
    return "".join(cipher_blocks)

def encryption_round(plain_block, round_key, round_number):
    blocks = split_blocks(plain_block, 8)
    permuted_blocks = []
    for block in blocks:
        block = (s_box_get(block))
        permuted_blocks.append(block)

    matrix = shift_rows(block_to_matrix(permuted_blocks))
    if round_number != 9:
        matrix = mix_columns(matrix)
    
    main_block = matrix_to_block(matrix)
    main_block = XOR(main_block, round_key)
    return main_block

def block_to_matrix(block):
    eight_bit_blocks = block
    hex_blocks = [binary_to_hex(b) for b in eight_bit_blocks]
    matrix = [["","","",""],
              ["","","",""],
              ["","","",""],
              ["","","",""]]
    
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
    
    matrix[1] = shift_left(matrix[1],1)
    matrix[2] = shift_left(matrix[2],2)
    matrix[3] = shift_left(matrix[3],3)
    
    return matrix

def shift_left(row, num_shifts):
    temp = ["", "", "", ""]
    for r in range(len(row)):
        temp[(r-num_shifts)%4] = row[r]
    return temp

def mix_columns(matrix):
    #fixed matrix A
    A = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
    #empty initialized product matrix
    product_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(4):
        for j in range(4):
            A_row = A[i]
            input_column = [int(matrix[x][j],16) for x in range(4)]
            
            product_matrix[i][j] = field_sum_list([multiply(A_row[x],input_column[x]) for x in range(4)])
    
    
    return integer_matrix_to_hex(product_matrix)

def integer_matrix_to_hex(int_matrix):
    converted_matrix = [["","","",""],["","","",""],["","","",""],["","","",""]]
    for i in range(4):
        for j in range(4):
            converted_matrix[i][j] = binary_to_hex(bin(int_matrix[i][j])[2:].zfill(8))
    return converted_matrix

def decrypt(ciphertext, key)->str:
    return None

from utils import split_blocks, XOR, s_box_get, binary_to_hex, hex_to_binary
from generate_round_keys import generate_round_keys


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

    main_block = shift_rows(permuted_blocks)
    if round_number != 9:
        '''
        MixColumn
        '''
    main_block = [hex_to_binary(h) for h in sum(main_block, [])]
    #flattens the matrix into a list
    main_block = "".join(main_block)
    main_block = XOR(main_block, round_key)
    return main_block

def shift_rows(block):
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
    
    matrix[1] = shift_left(matrix[1],1)
    matrix[2] = shift_left(matrix[2],2)
    matrix[3] = shift_left(matrix[3],3)
    

    return matrix

def shift_left(row, num_shifts):
    temp = ["", "", "", ""]
    for r in range(len(row)):
        temp[(r-num_shifts)%4] = row[r]
    return temp

def decrypt(ciphertext, key)->str:
    return None

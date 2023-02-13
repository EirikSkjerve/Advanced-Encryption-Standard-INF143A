from utils import split_blocks, XOR, s_box_get, random_bitstring

round_coefficients = ["00000001", "00000010", "00000100", "00001000", "00010000",
                      "00100000", "01000000", "10000000", "00011011", "00110110"]

'''Generate 11 round keys
K0 is of course just the plain key'''
def generate_round_keys(key)->list:
    keys = [key]
    for i in range(1, 11):
        key_blocks_updated = []
        key_blocks = split_blocks(keys[i-1], 32)
        
        '''Need dummy variables for this'''
        step_1 = XOR(key_blocks[0], g_function(key_blocks[3], i-1))
        step_2 = XOR(key_blocks[1], step_1)
        step_3 = XOR(key_blocks[2], step_2)
        step_4 = XOR(key_blocks[3], step_3)
        
        key_blocks_updated.append(step_1)
        key_blocks_updated.append(step_2)
        key_blocks_updated.append(step_3)
        key_blocks_updated.append(step_4)
        keys.append("".join(key_blocks_updated))
        
    return keys

def g_function(block, round_number):
    old_blocks = split_blocks(block, 8)
    
    shifted_blocks = ['', '', '', '']
    
    shifted_blocks[3] = old_blocks[0]
    shifted_blocks[0] = old_blocks[1]
    shifted_blocks[1] = old_blocks[2]
    shifted_blocks[2] = old_blocks[3] 
    
    permuted_block = ""
    
    for i, b in enumerate(shifted_blocks):
        b = s_box_get(b)
        
        if i == 0:
            b = XOR(b, round_coefficients[round_number])
        permuted_block += b
                
    return permuted_block

from utils import split_blocks, XOR

round_coefficients = ["00000001", "00000010", "00000100", "00001000", "00010000",
                      "00100000", "01000000", "10000000", "00011011", "00110110"]
'''Generate 11 round keys
K0 is of course just the plain key'''
def generate_round_keys(key)->list:
    round_number = 0
    key_blocks = split_blocks(key, 32)
    return None

def g_function(block, round_number):
    old_blocks = split_blocks(block, 8)
    new_blocks = ['', '', '', '']
    new_blocks[3] = old_blocks[0]
    new_blocks[0] = old_blocks[1]
    new_blocks[1] = old_blocks[2]
    new_blocks[2] = old_blocks[3]    
    return None
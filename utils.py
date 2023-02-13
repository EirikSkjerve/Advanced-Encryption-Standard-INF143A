'''Random key and bitstring generator for testing. This is not safe for real usage'''
def random_bitstring(p):
     
    import random
    bitstring = ""
     
    for _ in range(p):
        bitstring += str(random.randint(0,1))
         
    return(bitstring)



'''Takes an input of any size and splits it into blocks of lenght n. If the last block is shorter than n, it is padded with 0's'''
def split_blocks(input_block, size)->list:
    split_blocks = []
    block = ""
    
    for i in range(len(input_block)):
        
        block += input_block[i]
        if ((i+1)%size==0):
            split_blocks.append(block)
            block = ""
            
    if block:
        split_blocks.append(block)
    
    split_blocks[-1] = pad_with_zeros(split_blocks[-1], size)
    return split_blocks

def pad_with_zeros(input_block, size):
    while len(input_block) < size:
        input_block += "0"
    return input_block

'''XOR-operation on two bitstrings, e.g. plaintext and key'''
def XOR(bitstr1, bitstr2)->str:
    if len(bitstr1) != len(bitstr2):
        print("The two inputs need to be the same size")
        raise ValueError
    bits = ""
    for i in range(len(bitstr1)):
        bits += str((int(bitstr1[i]) ^ int(bitstr2[i])))

    return bits

'''(8,8) byte substitution function that serves as the AES S-box'''
def s_box()->str:
    return None

'''Converts binary string to hexadecimal string, and vice versa'''
def binary_to_hex(string)->tuple:
    if len(string) != 8:
        raise ValueError
    
    a_hex = format(int(string[:4], 2), 'x')
    b_hex = format(int(string[4:], 2), 'x')
    return (a_hex, b_hex)


def hex_to_binary(string)->str:
    if len(string) != 2:
        raise ValueError
    return None
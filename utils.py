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

'''Converts binary string to hexadecimal string, and vice versa'''
def binary_to_hex(string)->str:
    if len(string) != 8:
        raise ValueError

    return format(int(string[:4], 2), 'x')+format(int(string[4:], 2), 'x')


def hex_to_binary(string)->str:
    if len(string) != 2:
        raise ValueError

    return bin(int(string[0], 16))[2:].zfill(4)+bin(int(string[1], 16))[2:].zfill(4)


'''(8,8) byte substitution function that serves as the AES S-box'''
'''Thanks to https://gist.github.com/bonsaiviking/5571001 for the copy paste'''
Sbox = [
            ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'],
            ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
            ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
            ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
            ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
            ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
            ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
            ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
            ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
            ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
            ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
            ['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
            ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
            ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
            ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
            ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']
            ]

'''Takes an 8-bit string and returns its related sbox byte, converted to binary again'''
def s_box_get(byte)->str:
    #if input is a bitstring of lenght 8:
    row = int(byte[:4], 2)
    column = int(byte[4:], 2)
    return hex_to_binary(Sbox[row][column])


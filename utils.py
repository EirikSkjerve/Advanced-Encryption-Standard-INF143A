import base64

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

def unlim_bin_to_hex(bitstring):
    characters = ""
    for s in range(0, len(bitstring), 8):

        characters += format(int(bitstring[s:s+8], 2), 'x')
    return characters

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

'''Takes an 8-bit string and returns its related sbox byte, converted to binary again
The AES Sbox
'''
def s_box_get(byte)->str:
    #if input is a bitstring of lenght 8:
    row = int(byte[:4], 2)
    column = int(byte[4:], 2)
    return hex_to_binary(Sbox[row][column])

'''Sbox inverse'''
Sbox_inv = [
            ["52", "09", "6A", "D5", "30", "36", "A5", "38", "BF", "40", "A3", "9E", "81", "F3", "D7", "FB"],
            ["7C", "E3", "39", "82", "9B", "2F," "FF", "87", "34", "8E", "43", "44", "C4", "DE", "E9", "CB"],
            ["54", "7B", "94", "32", "A6", "C2", "23","3D", "EE", "4C", "95", "0B", "42", "FA", "C3", "4E"],
            ["08", "2E", "A1", "66", "28", "D9", "24", "B2", "76", "5B","A2", "49", "6D", "8B", "D1", "25"],
            ["72", "F8", "F6", "64", "86", "68", "98", "16", "D4", "A4", "5C", "CC", "5D", "65", "B6", "92"],
            ["6C", "70", "48", "50", "FD", "ED", "B9", "DA", "5E", "15", "46", "57", "A7", "8D", "9D", "84"],
            ["90", "D8", "AB", "00", "8C", "BC", "D3", "0A", "F7", "E4", "58", "05", "B8", "B3", "45", "06"],
            ["D0", "2C", "1E", "8F", "CA", "3F", "0F", "02", "C1", "AF", "BD", "03", "01", "13", "8A", "6B"],
            ["3A", "91", "11", "41", "4F", "67", "DC", "EA", "97", "F2", "CF", "CE", "F0", "B4", "E6", "73"],
            ["96", "AC", "74", "22", "E7", "AD", "35", "85", "E2", "F9", "37", "E8", "1C", "75", "DF", "6E"],
            ["47", "F1", "1A", "71", "1D", "29", "C5", "89", "6F", "B7", "62", "0E", "AA", "18", "BE", "1B"],
            ["FC", "56", "3E", "4B", "C6", "D2", "79", "20", "9A", "DB", "C0", "FE", "78", "CD", "5A", "F4"],
            ["1F", "DD", "A8", "33", "88", "07", "C7", "31", "B1", "12", "10", "59", "27", "80", "EC", "5F"],
            ["60", "51", "7F", "A9", "19", "B5", "4A", "0D", "2D", "E5", "7A", "9F", "93", "C9", "9C", "EF"],
            ["A0", "E0", "3B", "4D", "AE", "2A", "F5", "B0", "C8", "EB", "BB", "3C", "83", "53", "99", "61"],
            ["17", "2B", "04", "7E", "BA", "77", "D6", "26", "E1", "69", "14", "63", "55", "21", "0C", "7D"]
            ]

def s_box_get_inv(byte)->str:
    #if input is a bitstring of lenght 8:
    row = int(byte[:4], 2)
    column = int(byte[4:], 2)
    return hex_to_binary(Sbox[row][column])

'''String to binary, given each character is represented by 8 bits'''
def string_to_binary(plaintext):

    word_in_binary = ""

    for p in plaintext:
        word_in_binary += (bin(ord(p))[2:].zfill(8))
    
    return word_in_binary

'''Binary to string, given each character is represented by 8 bits'''
def binary_to_string(bitstring):
    characters = ""
    for s in range(0, len(bitstring), 8):

        characters += chr(int(bitstring[s:s+8],2))
    return characters

def secret_to_binary(secret):
    if len(secret) != 16:
        print("secret needs to be of lenght 16")
        raise ValueError
    bin_key = ""

    for s in secret:
        bin_key += (bin(ord(s))[2:].zfill(8))
    if len(bin_key) != 128:
        print("Key is not lenght 128")
        raise ValueError
    return bin_key

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
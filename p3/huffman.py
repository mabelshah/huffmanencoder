#
# Mabel Shah
# 012783442
# 02-19-19
#
# Project 3a
# Section 05
# Purpose: Utilize a binary tree to encode file

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    # def set_left(self, node):
    #     self.left = node
    #
    # def set_right(self, node):
    #     self.right = node

def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    elif a.freq == b.freq:
        if a.char < b.char:
            return True
        else:
            return False
    return False

def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    newnode = None
    # not sure what to do if comes_before is false
    if a.char < b.char:
        newchar = a.char
    else:
        newchar = b.char
    newfreq = a.freq + b.freq
    newnode = HuffmanNode(newchar, newfreq)
    newnode.left = a
    newnode.right = b
    return newnode

def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file"""
    freq = [0] * 256
    try:
        f_in = open(filename,'r')
    except:
        raise FileNotFoundError
    for line in f_in:
        for char in line:
            freq[ord(char)] = freq[ord(char)] + 1
    f_in.close()
    return freq

def find_min(nodelist): #rename for clarity
    min_node = nodelist[0]
    for i in range(0, len(nodelist)):
        currentnode = nodelist[i]
        if comes_before(currentnode, min_node):
            min_node = currentnode
    return min_node

def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""
    nodelist = []
    for i in range(len(char_freq)):
        newnode = HuffmanNode(i, char_freq[i])
        if char_freq[i] is not 0:
            nodelist.append(newnode)
    if len(nodelist) == 0:
        return None
    while len(nodelist) > 1:
        node1 = find_min(nodelist)
        nodelist.remove(node1)
        node2 = find_min(nodelist)
        nodelist.remove(node2)
        newnode = combine(node1, node2)
        nodelist.insert(0, newnode)
    return nodelist[0]

def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location"""
    code = []
    for i in range(256):
        code.append(i)
    _create_code_helper(node, '', code)
    return code

def _create_code_helper(new, currentcode, code):
    if new is None:
        return None
    if new.left is not None:
        _create_code_helper(new.left, currentcode + "0", code)
    if new.right is not None:
        _create_code_helper(new.right, currentcode + "1", code)
    else:
        code[new.char] = currentcode
    return code

def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    header_vals = ""
    counter = 0
    for i in freqs:
        if i is not 0:
            header_vals = header_vals + str(counter) + " " + str(i) + ' '
        counter += 1
    header_vals = header_vals[:-1]
    return header_vals

def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""
    freqlist = cnt_freq(in_file)
    tree = create_huff_tree(freqlist)
    header = create_header(cnt_freq(in_file))
    f_in = open(in_file,'r')
    f_out = open(out_file,'w')
    if f_out is not None:
        f_out.write(header + "\n")
    code = create_code(tree)
    while True:
        char = f_in.read(1)
        if not char:
            break
        f_out.write(str(code[ord(char)]))
    f_in.close()
    f_out.close()

# def parse_header(filename):
#     #try:
#     #    f_in = open(filename)
#     #except:
#     #    raise FileNotFoundError
#     list_of_freqs = [0] * 256
#     header_string = filename.split()
#     for i in range(0, len(header_string) - 1, 2):
#         val = int(header_string[i])
#         freq = int(header_string[i + 1])
#         list_of_freqs[val] = freq
#     return list_of_freqs
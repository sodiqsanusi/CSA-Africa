import numpy as np

def bitstring_array(x):
    # force to big endian for printing
    endianed = x.dtype.newbyteorder('B')    
    return "".join('{0:08b}'.format(d) for d in x.astype(endianed).tostring())


import itertools    

import textwrap

def get_binary(data, word_size, offset, n_words):
    binary = "".join(["{0:08b}".format(byte) for byte in data])        
    selection = binary[offset:offset+n_words*word_size]
    return selection

def raw_binary_view(data, word_size, offset, n_words):
    if n_words<0:
        print(get_binary(data, len(data)*8, offset, 1))
        return
        
    selection = get_binary(data, word_size, offset, n_words)
    out = [selection[i*word_size:(i+1)*word_size] for i in range(n_words)]
    print("Bit offset: %08d      Word size: %3d     Words: %4d" % (offset, word_size, n_words))
    print()
    print("\n".join(textwrap.wrap(" ".join(out), width=80)))
    
    
def binary_to_array(data, dtype, offset, shape):
    n_words = np.prod(shape)
    word_size = np.finfo(dtype).bits
    binary = get_binary(data, word_size, offset, n_words)
    binary = binary + "0" * (8-len(binary)%8)
    rbytes = (bytearray(([(int(binary[i*8:(i+1)*8], 2)) for i in range(len(binary)//8)])))    
    return np.fromstring(bytes(rbytes), dtype=dtype, count=n_words).reshape(shape).byteswap()
  
    
def intersperse(s, step, char):
    out = []
    step_cycle = itertools.cycle(step)
    char_cycle = itertools.cycle(char)
    i = 0
    while i<len(s):
        interval = next(step_cycle)
        split_char = next(char_cycle)
        out.append(s[i:i+interval])    
        out.append(split_char)
        i += interval    
    return "".join(out)


def print_float_binary(x):
    print(bitstring_array(np.array(x)))
    
def print_binary_float(fl, word, exp, mantissa):
        
        mantissa -= 1
        bias = (2**(exp-1))-1
        total_width = exp + mantissa + 1 # for sign
        
        sep_word = intersperse(word, [1,exp,mantissa], ['|','|','|'])
        sign, e, m = int(word[0:1],2), int(word[1:1+exp],2)-bias, int(word[1+exp:total_width],2)        
        infinite = e==2**(exp-1)
            
        sign = -1 if sign==1 else 1
        
        print((("{0:4s}|  {1:%ds} |  {2:%ds}|"%(exp-3, mantissa-2)).format("Sign", "Exp", "Mantissa")))
        print("   "+sep_word)
        print((("{0:4d}|  {1:%dd} |  {2:%dd}|"%(exp-3, mantissa-2)).format(sign, e, m)))
        
        if infinite:
            print("Infinite/NaN")
        else:
            print("    {0} * {1} * 2^{2}".format(sign, 1.0+m/(2.0**mantissa), e))
            print("    = {0} * {1} * {2}".format(sign, 1.0+m/(2.0**mantissa), 2**e))
            print("    = %.20f" % fl)
    
        print("")

def print_float(fl, dtype=np.float64):
    print_binary_float(fl, bitstring_array(np.array(fl, dtype=dtype)), 11, 53)

def print_float_structure(x):
    flat = x.ravel()
    nbits = x.dtype.itemsize*8
    exp, mantissa = {
        16: (5,11),
        32: (8, 24),
        64: (11, 53),
        128: (15, 113),
    }[nbits]
    total_width = exp + mantissa 
    
    bitstring = bitstring_array(x)            
    
    for bit, fl in zip(range(0,len(bitstring),total_width), flat):                
        word = bitstring[bit:bit+total_width]        
        print_binary_float(fl, word, exp, mantissa)
        
        
def print_raw_binary_array(x):
    print(intersperse(bitstring_array(x), [x.dtype.itemsize*8], ['\n']))    
    
def print_flat_array(x):
        print(" ".join(["%f"%f for f in x.ravel()]))
        
def print_shape(x):    
    # array inspector
    print("\tShape:\t\t\t{0}".format(x.shape))
    print("\tStride:\t\t\t{0}".format(x.strides))    
    print("\tData type:\t\t{0}".format(x.dtype))
    print("\tElements:\t\t{0}".format(x.size))
    print("\tNo. of bytes:\t\t{0}".format(x.nbytes))    
    print("\tBits per element:\t{0}".format(8*x.itemsize))    
    print("-"*80)
    print("")
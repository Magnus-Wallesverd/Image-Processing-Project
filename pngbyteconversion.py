import zlib
import binascii

'''
TODO After Math

0. Refactor to use methods
1. Convert clean data back to original format
2. Compress
3. Create new image with returned data
'''

with open("peppers.png","rb") as f:
    data = f.read()

def png2byte(cleanhexarr):
    
    width = 0
    height = 0
    fb = 1
    bpp = 3

    for i in range(8,len(data)):
        temp = data[i:i+4]
        if(temp == b'IHDR'): 
            width = int.from_bytes(data[i+4:i+8], byteorder='big')
            height = int.from_bytes(data[i+8:i+12], byteorder='big')
            bitdepth = int(data[i+12])
            break

    startpos = 0                        # Iterator
    endpos = 0

    # detect IDAT CHUNK 
    for i in range(8,len(data)):
        temp = data[i:i+4]
        if(temp == b'IDAT'):
            startpos = i+4
            break

    # detect IEND CHUNK 
    for i in range(len(data),8,-1):
        temp = data[i-4:i]
        if(temp == b'IEND'):
            endpos = i-4
            break

    idatstr = data[startpos:endpos]     # stores IDAT as a str obj
    idat = zlib.decompress(idatstr)     # decompresses IDAT

    tb = len(idat)                      # total bytes in IDAT
    scanline = (width*bpp) + fb         # total bytes per line

    startpos2 = 0                       # Iterator
    endpos2 = scanline

    # prints scanlines 
    for i in range(height): 
        cleanhex = binascii.hexlify(idat[startpos2:endpos2])
        cleanhexarr.append(cleanhex)
        startpos2 += scanline
        endpos2 += scanline
    
    return cleanhexarr

# does convolution
# consider the filter byte

def avg_filter(hexarr):
    prekernel = []
    for i in range(3):
        startpos = 2
        endpos = 4
        temp = hexarr[i]
        for j in range(3):
            prekernel.append(temp[startpos:endpos])
            startpos+=2
            endpos+=2
    return prekernel
    
arr = []
filterarr = avg_filter(png2byte(arr))
print(filterarr)
# print(filterarr[3:8])

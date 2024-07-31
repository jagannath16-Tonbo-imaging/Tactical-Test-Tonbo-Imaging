
"""
Created on Fri Jun 30 18:39:02 2017

@author: Aneesh
"""
import re
import numpy 
import matplotlib.pyplot as plt
# from img_util import dphe
def read_mat(filename):
    with open(filename, 'r') as f:
        buffer = f.read()
    try:
        header, width, height=re.search("(^PG\s(?:\s*#.*[\r\n])*""(\d+)\s(?:\s*#.*[\r\n])*""(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
        
        
    except AttributeError:
        raise ValueError("Not a valid file: '%s'" % filename)
    
    newbuf=list(map(float,(buffer[len(header):]).split()))
    newbuf=numpy.asarray(newbuf) 
    newbuf=newbuf.reshape(int(height),int(width))
    f.close()
    return newbuf

def read_pgm(filename):
    with open(filename, 'r') as f:
        buffer = f.read()
    try:
        header, width, height, maxval=re.search("(^P2\s(?:\s*#.*[\r\n])*"
                                        "(\d+)\s(?:\s*#.*[\r\n])*"
                                        "(\d+)\s(?:\s*#.*[\r\n])*"
                                        "(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
        
        
    except AttributeError:
        raise ValueError("Not a valid file: '%s'" % filename)
    
    newbuf=list(map(int,(buffer[len(header):]).split()))
    newbuf=numpy.asarray(newbuf) 
    newbuf=newbuf.reshape(int(height),int(width))
    f.close()
    return newbuf

def write_pgm(filename, img, maxval):
    width = numpy.shape(img)[1]
    height = numpy.shape(img)[0]
    print(width)
    with open(filename, 'w') as f:
        f.write('P2\n')
        f.write('#Comment\n')
        f.write(str(width)+' '+str(height)+'\n')
        f.write(str(maxval)+'\n')
        for col in range(height):
            for row in range(width):
                f.write(str(numpy.int(img[col,row]))+' ')
            f.write('\n')
    
    f.close()

def read_raw(filename, width, height, bits=16):
    f=open(filename, "rb")
    if(bits==16):
        img = numpy.fromfile(f, dtype=numpy.int16)
    else:
        img = numpy.fromfile(f, dtype=numpy.uint8)
    f.close()
    if(numpy.size(img)!=width*height):
        print("Error: width, hight do not match the file size")
        return None
    img = numpy.reshape(img, (height, width))
    return img

def write_raw(filename, img):
    f=open(filename, "wb")
    img = numpy.reshape(img, (numpy.size(img),))
    img.tofile(f)
    f.close()

if __name__ == "__main__":
    
    file_name="./NUC_image2"
    img=read_raw(file_name+".bin",640,480,bits=16)
    write_pgm( file_name+".pgm", img, 16383)
    img_dphe = dphe(numpy.uint16(img))
    plt.figure(figsize=(15,15))
    plt.imshow(img_dphe,'gray')
    plt.savefig(file_name+".jpg")
    
            

    
    
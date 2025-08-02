
#   Student ID: 20469160
#   Student Name: W.M.Naradha
#
#   file_manager: It contains the main file management and extraction functions and objects.
#
import numpy as np


def read_csv(source,x1=0, y1=0, s='r', outarray=False, dt=int, splt=','): #Function to read a csv file (Part of it given x1 and y1 or the entire file.)
    outcapt = []
    capt = []
    fo = open(source, s)
    [capt.append(line.strip().split(splt)) for line in fo.readlines()]
    fo.close()
    if x1 == 0 and y1 == 0:
        x1 = len(capt)
        for line in capt:
            if (len(line))==y1 or y1==0:
                y1 = len(line)
            else:
                raise Exception('Entered Terrain not supported please renter terrain.')
    oa = np.zeros((x1, y1), dtype=dt)
    if outarray == True:
        for x in range(x1):
            for y in range(y1):
                #print(capt[x][y])
                oa[x, y] = dt(capt[x][y])
        return (oa)
    elif outarray == False:
        for x in range(x1):
            col = []
            for y in range(y1):
                col.append(dt(capt[x][y]))
            outcapt.append(col)
        return outcapt

def write_csv(incomp, source, s='w',splt=','):  #Writing a grid into a csv file.
    if 'numpy.ndarray' in str(type(incomp)):
        fn = np.size
    elif 'list' in str(type(incomp)):
        fn = len
    fo = open(source, s)
    for line in incomp:
        for i,char in enumerate(line):
            if (i+1)%fn(line)==0 and i!=0:
                fo.write(str(char).strip('[').strip(']'))
            else:
                fo.write(str(char).strip('[').strip(']') + splt)
        fo.write('\n')
    fo.close()
    return True

def read_csv_profile(source, s='r', outarray=False, dt=int, splt=','):  #Reading class object profiles
    capt = []
    fo = open(source, s)
    [capt.append(line.strip().split(splt)) for line in fo.readlines()]
    fo.close()
    return capt

def write_csv_profile(incomp, source, s='w',splt=',',end='\n'): #Writing the class object profiles
    if 'numpy.ndarray' in str(type(incomp)):
        fn = np.size
    elif 'list' in str(type(incomp)):
        fn = len
    fo = open(source, s)
    for i,line in enumerate(incomp):
        if i < len(incomp)-1:
            text = line+splt
            fo.write(text)
        else:
            fo.write(line)
    fo.write(end)
    fo.close()
    return True

def write_strng(strng,source,s='w'):
    fo = open(source, s)
    fo.write(strng)
    fo.close()
    return True

def read_strng(source,s='r'):
    strng = ''
    fo = open(source, s)
    for line in fo.readlines():
        strng += (str(line) + '\n')
    fo.close()
    return strng

#For Testing Purposes:

#CSV write and read tester
#a = np.zeros((10, 10), dtype=int)
#print(write_csv(a, 'yo.csv', s='w+'))
#print(read_csv(12, 2, 'cat.csv', s='r',dt=str,splt=' '))
#print(read_csv('../inputs/terrain1.csv', s='r',outarray=True,dt=float))

#Text file write and read tester
#strng = '''
#Hello! How are you?
#'''
#print(write_strng(strng,'yello.txt',s='w+'))
#print(read_strng('yello.txt'))

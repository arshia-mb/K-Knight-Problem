import sys
import os

def print_to_file(input_stream,filename):
    f = open(filename, "w")
    for inputs in input_stream:
        if not inputs == None:
            f.write(inputs)
    f.close()

def create_dir(path):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname,path)
    os.mkdir(filename)
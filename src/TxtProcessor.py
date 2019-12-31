
import os

path = os.path.dirname(os.path.abspath(__file__))
txt_file = os.path.join( path, '..', 'inputs.txt')

def get_readList () :

    with open(txt_file, 'r') as f:
        return f.readlines()
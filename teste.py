import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


from main.src.dash_preparedata import PrepareData

def media(x1, x2):
    x = np.mean(x1+x2)

    return x

if __name__ == '__main__':
    x1= 2
    x2= 4
    
    x= media(x1, x2)
    print(x)
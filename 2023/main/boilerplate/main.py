import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data1'

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    for l in lines:
        pass
    print('done')
    print(s)
        
do_your_magic1()
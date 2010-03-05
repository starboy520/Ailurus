#!/usr/bin/env python
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
# License: GPL

import sys

def to10(int16):
    assert isinstance(int16, int)
    if int16>=ord('A'):   return int16-ord('A')+10
    else:                 return int16-ord('0')

if len(sys.argv)==1: sys.exit(0)

string = sys.argv[1]
loc = 0
while loc < len(string):
    p = string[loc]
    if p=='%':
        a = ord(string[loc+1])
        b = ord(string[loc+2])
        sys.stdout.write( chr( to10(a)*16 + to10(b) ) )
        loc += 3
    else:
        sys.stdout.write( p )
        loc += 1
sys.exit(0)
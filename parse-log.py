#!/usr/bin/python

import json
from pprint import pprint

f1 = open("chlog.json", "r")
f2 = open("chlog2.json", "w")

count = 0
for line in f1:
    count = count + 1
f1.close()

line_num = 0
f2.write('[')

f1 = open("chlog.json", "r")
for line in f1:
    if (line_num < count-1):
        f2.write(line + ',') 
    else:
        f2.write(line) 
    line_num = line_num + 1

f2.write(']')

with open('chlog2.json') as data_file:    
    data = json.load(data_file)
    pprint (data)

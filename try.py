#!/usr/bin/python

import json
from pprint import pprint

with open('chlog2.json') as data_file:
    data = json.load(data_file)

last_offset = 0
for line in data:
    if ((last_offset != line['audioTimeOffset']) & (line['type'] == 'final')):
       secs = line['audioTimeOffset'] / 10000000
       hr = secs /  3600
       min = secs / 60
       s = secs % 60
       pprint (secs*1000)
       #pprint (str(hr) + ':' + str(min) + ':' + str(s))
       last_offset = line['audioTimeOffset']

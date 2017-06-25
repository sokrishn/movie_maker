import os
import StringIO
import struct
import thread
import time
import uuid
import wave
import sys
import subprocess
import websocket
import json
from pprint import pprint

from auth import AzureAuthClient
from subprocess import call

os.system('grep type log > log.json')

f1 = open("log.json", "r")
f2 = open("log2.json", "w")

count = 0
for line in f1:
    count = count + 1
f1.close()

line_num = 0
f2.write('[')

f1 = open("log.json", "r")
for line in f1:
    if (line_num < count-1):
        f2.write(line + ',')
    else:
        f2.write(line)
    line_num = line_num + 1

f2.write(']')
f2.close()

with open('log2.json') as data_file:
    data = json.load(data_file)

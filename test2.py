"""
Python sample demonstrating use of Microsoft Translator Speech Translation API.
"""

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

last_offset = 0
num_tts_clip = 0
for line in data:
    if ((last_offset != line['audioTimeOffset']) & (line['type'] == 'final')):
        num_tts_clip = num_tts_clip + 1
        last_offset = line['audioTimeOffset']

output_folder = '/Users/sowkrish/Downloads/Movie-Translator-Bot/947d5d8f6bf74ac49880fe2796db626a'
mix_command = "./ffmpeg "
count = 0
while count < num_tts_clip:
    count = count + 1
    mix_command = mix_command + "-i " + output_folder + "/tts_" + str(count) + ".wav "

muted_source_file = "muted.mp4"
mix_command = mix_command + "-i " + muted_source_file
mix_command = mix_command + " -filter_complex "

count = 0
last_offset = 0
for line in data:
    if ((last_offset != line['audioTimeOffset']) & (line['type'] == 'final')):
        if (count == 0):
            mix_command = mix_command + "\""
        secs = line['audioTimeOffset'] / 10000000
        hr = secs /  3600
        min = secs / 60
        s = secs % 60
        pprint (secs*1000)
        if (secs > 0):
            mix_command = mix_command + "[" + str(count) + "]adelay=" + str(secs*1000) + "|" + str(secs*1000) + "[s" + str(count) + "];"
        count = count + 1
        last_offset = line['audioTimeOffset']

count = 0
last_offset = 0
for line in data:
    if ((last_offset != line['audioTimeOffset']) & (line['type'] == 'final')):
        secs = line['audioTimeOffset'] / 10000000
        hr = secs /  3600
        min = secs / 60
        s = secs % 60
        pprint (secs*1000)
        if (secs > 0):
            mix_command = mix_command + "[s" + str(count) + "]"
        else:
            mix_command = mix_command + "[" + str(count) + "]"
        count = count + 1
        last_offset = line['audioTimeOffset']

#count = 0
#while (count < num_tts_clip):
#    mix_command = mix_command + "[s" + str(count) + "]"
#    count = count + 1

mix_command = mix_command + "amix=" + str(num_tts_clip) + "[mixout]"
if count > 0:
   mix_command = mix_command + "\""

mix_command = mix_command + " -map " + str(num_tts_clip) + ":v -map [mixout]"
mix_command = mix_command + " -c:v copy Your-Movie.mp4"

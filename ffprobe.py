#/* cSpell:disable */ 

import os, subprocess, json, re

# ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4
# ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1:nk=1

fn = "Aki秋水_2023-06-03_10-00-05.ts"

result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "program_stream=width,height", "-of", "default=nw=1:nk=1", fn], capture_output=True, text=True)

print(result.stdout)

x = re.search("540\n960", result.stdout)


if x: 
    print("found")
else:
    print("not found")

#!/usr/bin/env python3

import subprocess
import sys
import os
import psutil
import json

if len(sys.argv) == 1 or len(sys.argv) > 2:
    print("Error: invalid number of arguments")
    sys.exit(1)

from vosk import Model, KaldiRecognizer, SetLogLevel

for proc in psutil.process_iter():
    if proc.name() == "anki":
        for dir in proc.open_files():
            if dir.path.endswith("collection.anki2"):
                anki_path = dir.path.replace("anki2", "media")

SAMPLE_RATE = 16000

SetLogLevel(-1)

model = Model("/home/asakura/.local/share/vosk/essmall")
rec = KaldiRecognizer(model, SAMPLE_RATE)

X = sys.argv[1].replace("[sound:", "").replace("]", "")

with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                            anki_path + "/" + X,
                            "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                            stdout=subprocess.PIPE) as process:

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            nl = res['text']
            print (res['text'], end=", ")
 #       else:
 #           print(rec.PartialResult())

#    print(rec.FinalResult())
res = json.loads(rec.FinalResult())
print (res['text'], end=".\n")

#!/usr/bin/env python3

import os
import signal
import subprocess

signal.signal(signal.SIGINT, lambda *_: (print("\nBenchmark Interrupted."), os._exit(1)))

INDEX = ["0,0", "0,1", "0,2", "1,0", "1,1", "1,2", "1,3", "2,0"]
PROMPTS = open("benchmark.prompts").read().splitlines()

for i in INDEX:
    print(f"INDEX: {i}")
    for prompt in PROMPTS:
        print(f"PROMPT: {prompt}")
        os.environ["INDEX"] = i
        subprocess.run(f'/app/app.py "{prompt}" 3', shell=True)


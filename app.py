#!/usr/bin/env python3

import sys
import config

from dotenv import load_dotenv
load_dotenv()

"""
Usage: INDEX=M,N python app.py [prompt] [num_images] [num_saved_steps]
"""

if len(sys.argv) > 1:
    prompt = sys.argv[1]
    randomizer_on = False
    if prompt == "randomizer":
        randomizer_on = True
        print("Randomizer ON...")
    else:
        prompt = prompt + ", photography, realistic, high quality, detailed, sharp focus, best quality"
    negative_prompt = "cartoon, manga, 3d render, cgi, plastic, doll, fake, painting, unreal engine, ugly, deformed, disfigured, poor quality, low resolution, low quality, no frames, no window, no writing, text"

    num_images      = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    if num_images < 1:
        num_images = 1000000000
        print("Generating images until interrupted...")
    
    num_saved_steps = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    width  = 1024
    height = 1024
    guidance_scale = 8
    num_inferences = 18
else:
    prompt = None

if __name__ == "__main__":
    try:
        if prompt:
            print('Entering cli mode...')
            import text2image
            pipe = text2image.pipeline(config.MODEL_INDEX, config.MODEL_SUBINDEX)
            import cli
            cli.main(pipe, prompt, negative_prompt, num_images, num_saved_steps, width, height, guidance_scale, num_inferences, randomizer_on)
        else:
            import web
            print('Entering web mode...')

    except KeyboardInterrupt:
        print("\nScript interrupted!")
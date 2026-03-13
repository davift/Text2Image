#!/usr/bin/env python3

import os
import sys
import shutil
from gradio_client import Client
import config
from dotenv import load_dotenv

load_dotenv()

def generate_image(prompt):
    hf_token = os.getenv("HF_TOKEN")
    destination_path = os.path.join(config.RELA_PATH, "generated_image.png")

    try:
        spaces = [
            "heartsync/pornhub",
            "retwpay/pornmasterPro_noobV3VAE",
        ]

        client = Client(spaces[0], token=hf_token)
        
        print(f"Generating...")
        result = client.predict(
            prompt=prompt,
            negative_prompt="ugly, deformed, disfigured, poor quality, low resolution",
            seed=0,
            randomize_seed=True,
            width=1024,
            height=1024,
            guidance_scale=7,
            num_inference_steps=28,
            api_name="/infer"
        )

        if result:
            shutil.copy(result, destination_path)
            os.chmod(destination_path, 0o777)
            print(f"✅ Saved to: {destination_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    my_prompt = sys.argv[1] if len(sys.argv) > 1 else "Futuristic woman, cyberpunk style, realistic."
    generate_image(my_prompt)


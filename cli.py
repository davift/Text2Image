import os
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:128,expandable_segments:True")

import config
import time
import randomizer
timestamp = int(time.time())

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main(pipe, prompt, negative_prompt, num_images, num_saved_steps, width, height, guidance_scale, num_inferences, randomizer_on):
    print("Running...")
    def save_step(pipe, step_index, timestep, callback_kwargs):
        if step_index <= num_inferences - num_saved_steps:
            return callback_kwargs

        latents = callback_kwargs["latents"]
        with torch.no_grad():
            image = pipe.vae.decode(latents / pipe.vae.config.scaling_factor, return_dict=False)[0]
            image = pipe.image_processor.postprocess(image, output_type="pil")[0]
            step_filename = f"{timestamp}_{config.MODEL_INDEX},{config.MODEL_SUBINDEX}_{step_index:02d}.png"
            image.save(config.FULL_PATH + step_filename)
            os.chmod(config.FULL_PATH + step_filename, 0o777)
        return callback_kwargs
    
    for image_index in range(num_images):
        seed = torch.seed()
        generator = torch.Generator(device=device).manual_seed(seed)

        if randomizer_on:
            prompt = randomizer.randomizer()
            print(f"Prompt: {prompt}", flush=True)

        start_time = time.time() 
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inferences,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            generator=generator,
            callback_on_step_end=save_step,
            callback_on_step_end_tensor_inputs=["latents"],
            # num_images_per_prompt=4,
        ).images[0]
        end_time = time.time()
        elapsed = int(end_time - start_time)
        
        if randomizer_on:
            trailling = prompt.replace(",", "").replace(" ", "-")
        else:
            if num_saved_steps > 1:
                trailling = num_inferences
            else:
                trailling = image_index

        filename = f"{timestamp}_{config.MODEL_INDEX},{config.MODEL_SUBINDEX}_{trailling}.png"
        image.save(config.FULL_PATH + filename)
        os.chmod(config.FULL_PATH + filename, 0o777)
        del image
        torch.cuda.empty_cache()
        print(f"[{elapsed}s] {config.FULL_PATH}{filename}")

    print("Done!")


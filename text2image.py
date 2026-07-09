import config
import os
os.environ["PYTORCH_ALLOC_CONF"] = "max_split_size_mb:128,expandable_segments:True"

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def pipeline(index, subindex):
    print(f"Loading pipeline {index},{subindex}...")

    if index == 0:
        from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler
        models = [
            "votepurchase/waiREALCN_v150",            # Striggles to generate people of color. They look asian.
            "votepurchase/waiREALCN_v14",             # Striggles to generate people of color. They look asian.
            "votepurchase/pornmasterPro_noobV3VAE",   # Striggles to generate people of color. Pointy teeth when smiling.
            "votepurchase/pornmasterPro_realismILV4", # Struggles to generate people of color. Maybe less the above ones.
        ]
        pipe = StableDiffusionXLPipeline.from_pretrained(
            models[subindex],
            cache_dir=config.MODELS,
            torch_dtype=torch.float16,                # Do not change to `dtype`, it will cause OOM error.
            variant="fp16",
            use_safetensors=True,
            # local_files_only=True
        )
        pipe.to(device)
        pipe.enable_model_cpu_offload()
        pipe.vae.enable_slicing()
        pipe.enable_attention_slicing()

        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

    if index == 1:
        from diffusers import AutoPipelineForText2Image, DEISMultistepScheduler
        models = [
            "Lykon/absolute-reality-1.81",            # Less bias towards people of color.
            "Lykon/DreamShaper-8",                    # Less bias towards people of color.
            "Lykon/NeverEnding-Dream",                # Not super realistic. No safe tensors.
        ]
        pipe = AutoPipelineForText2Image.from_pretrained(
            models[subindex],
            cache_dir=config.MODELS,
            torch_dtype=torch.float16,
            use_safetensors=True,
            # local_files_only=True
        )
        pipe.to(device)
        pipe.enable_model_cpu_offload()
        pipe.safety_checker = None
        pipe.feature_extractor = None
        pipe.requires_safety_checker = False

        pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)

    if index == 2:
        from diffusers import DiffusionPipeline
        models = [
            "Heartsync/NSFW-Uncensored",              # Tends to produce anime style.
        ]
        pipe = DiffusionPipeline.from_pretrained(
            models[subindex],
            cache_dir = config.MODELS,
            torch_dtype=torch.float16,
            use_safetensors = True,
            # local_files_only=True
        )
        pipe.to(device)
        pipe.enable_model_cpu_offload()
        pipe.vae.enable_slicing()
        pipe.enable_attention_slicing()
        # pipe.vae.enable_tiling()

    # if index == 3:
    #     from diffusers import ZImagePipeline          # Could not make it to work in my hardware.
    #     models = [
    #         "Tongyi-MAI/Z-Image-Turbo",
    #     ]
    #     pipe = ZImagePipeline.from_pretrained(
    #         models[subindex],
    #         cache_dir=config.MODELS,
    #         torch_dtype=torch.bfloat16,
    #         low_cpu_mem_usage=True,
    #         use_safetensors=True,
    #     )
    #     pipe.enable_model_cpu_offload()
    #     pipe.vae.enable_slicing()
    #     pipe.enable_attention_slicing()
    #     pipe.vae.enable_tiling()

    return pipe
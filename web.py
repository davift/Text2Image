import os
os.environ["PYTORCH_ALLOC_CONF"] = "max_split_size_mb:128,expandable_segments:True"

import config

import gradio as gr
import gradio_client.utils as _gc_utils
import torch
import gc
from datetime import datetime
import text2image

# Monkey-patch: fix gradio_client crash when additionalProperties is a bool
_orig_json_schema_to_python_type = _gc_utils._json_schema_to_python_type
def _patched_json_schema_to_python_type(schema, defs=None):
    if isinstance(schema, bool):
        return "Any"
    return _orig_json_schema_to_python_type(schema, defs)
_gc_utils._json_schema_to_python_type = _patched_json_schema_to_python_type

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipe = text2image.pipeline(config.MODEL_INDEX, config.MODEL_SUBINDEX)

def infer(prompt, negative_prompt, width, height, guidance_scale, steps, progress=gr.Progress(track_tqdm=True)):
    seed = torch.seed()
    generator = torch.Generator(device=device).manual_seed(seed)

    try:
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            generator=generator,
            # num_inference_steps=9,  # This actually results in 8 DiT forwards
            # guidance_scale=0.0,     # Guidance should be 0 for the Turbo models
        ).images[0]
        image.format = "PNG"

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{seed}.png"
        image.save(os.path.join(config.FULL_PATH, filename))

        return image, seed

    finally:
        gc.collect()
        torch.cuda.empty_cache()

css = """
.progress-view {
    opacity: 0.2 !important;
    background: rgba(255, 255, 255, 0.2) !important;
}

.generating {
    visibility: visible !important;
}
"""

print(f"Loading web-ui with model index: {config.MODEL_INDEX},{config.MODEL_SUBINDEX}")
with gr.Blocks(theme=gr.themes.Soft(), css=css, title="Text2Image | by DFT.WIKI") as demo:
    gr.Markdown("## 🖌️ Uncensored Text-to-Image (NSFW) | Use with resposibility and respect!")

    with gr.Row():
        with gr.Column():
            prompt_in = gr.Textbox(label="Prompt", value="Futuristic, sexy woman with sharp facial features, blonde hair, smiling, neon cyberpunk metropolis, ultra-realistic render, dramatic lighting", lines=5)
            neg_in = gr.Textbox(label="Negative Prompt", value="ugly, deformed, disfigured, poor quality, low resolution, low quality, no frames, no window, no writing, text", lines=2)
            
        with gr.Column():
            with gr.Row():
                w_in = gr.Slider(256, 2048, 1024, step=32, label="Width")
                h_in = gr.Slider(256, 2048, 1024, step=32, label="Height")
                
            with gr.Row():
                guidance_scale_in = gr.Slider(1, 10, 6, step=0.5, label="Guidance")
                steps_in = gr.Slider(1, 25, 18, step=1, label="Steps")

            with gr.Row():
                out_seed = gr.Number(label="Seed Used")

    run_btn = gr.Button("Generate", variant="primary")
    out_img = gr.Image(label="Result", format="png")

    run_btn.click(
        fn=infer,
        inputs=[prompt_in, neg_in, w_in, h_in, guidance_scale_in, steps_in],
        outputs=[out_img, out_seed],
        show_progress="minimal"
    )

    with gr.Row():
        bottom_img1 = gr.Image(value="output1.png", show_label=False)
        bottom_img2 = gr.Image(value="output2.png", show_label=False)
        bottom_img3 = gr.Image(value="output3.png", show_label=False)
        bottom_img4 = gr.Image(value="output4.png", show_label=False)

demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    favicon_path="icon.png"
)


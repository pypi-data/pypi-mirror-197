import gradio as gr
import torch
from diffusers import DDIMScheduler, StableDiffusionPipeline

from diffusion_webui.utils.model_list import stable_model_list


def stable_diffusion_text2img(
    model_path: str,
    prompt: str,
    negative_prompt: str,
    guidance_scale: int,
    num_inference_step: int,
    height: int,
    width: int,
):

    pipe = StableDiffusionPipeline.from_pretrained(
        model_path, safety_checker=None, torch_dtype=torch.float16
    ).to("cuda")

    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    pipe.enable_xformers_memory_efficient_attention()

    images = pipe(
        prompt,
        height=height,
        width=width,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_step,
        guidance_scale=guidance_scale,
    ).images

    return images[0]


def stable_diffusion_text2img_app():
    with gr.Blocks():
        with gr.Row():
            with gr.Column():
                text2image_model_path = gr.Dropdown(
                    choices=stable_model_list,
                    value=stable_model_list[0],
                    label="Text-Image Model Id",
                )

                text2image_prompt = gr.Textbox(
                    lines=1, value="Prompt", label="Prompt"
                )

                text2image_negative_prompt = gr.Textbox(
                    lines=1,
                    value="Negative Prompt",
                    label="Negative Prompt",
                )

                with gr.Accordion("Advanced Options", open=False):
                    text2image_guidance_scale = gr.Slider(
                        minimum=0.1,
                        maximum=15,
                        step=0.1,
                        value=7.5,
                        label="Guidance Scale",
                    )

                    text2image_num_inference_step = gr.Slider(
                        minimum=1,
                        maximum=100,
                        step=1,
                        value=50,
                        label="Num Inference Step",
                    )

                    text2image_height = gr.Slider(
                        minimum=128,
                        maximum=1280,
                        step=32,
                        value=512,
                        label="Image Height",
                    )

                    text2image_width = gr.Slider(
                        minimum=128,
                        maximum=1280,
                        step=32,
                        value=768,
                        label="Image Width",
                    )

                text2image_predict = gr.Button(value="Generator")

            with gr.Column():
                output_image = gr.Image(label="Output")

        text2image_predict.click(
            fn=stable_diffusion_text2img,
            inputs=[
                text2image_model_path,
                text2image_prompt,
                text2image_negative_prompt,
                text2image_guidance_scale,
                text2image_num_inference_step,
                text2image_height,
                text2image_width,
            ],
            outputs=output_image,
        )

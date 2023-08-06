import gradio as gr
import torch
from diffusers import DDIMScheduler, StableDiffusionImg2ImgPipeline
from PIL import Image

from diffusion_webui.utils.model_list import stable_model_list


def stable_diffusion_img2img(
    image_path: str,
    model_path: str,
    prompt: str,
    negative_prompt: str,
    guidance_scale: int,
    num_inference_step: int,
):

    image = Image.open(image_path)

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_path, safety_checker=None, torch_dtype=torch.float16
    )
    pipe.to("cuda")
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    pipe.enable_xformers_memory_efficient_attention()

    output = pipe(
        prompt=prompt,
        image=image,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_step,
        guidance_scale=guidance_scale,
    ).images

    return output[0]


def stable_diffusion_img2img_app():
    with gr.Blocks():
        with gr.Row():
            with gr.Column():
                image2image2_image_file = gr.Image(
                    type="filepath", label="Image"
                )

                image2image_model_path = gr.Dropdown(
                    choices=stable_model_list,
                    value=stable_model_list[0],
                    label="Image-Image Model Id",
                )

                image2image_prompt = gr.Textbox(
                    lines=1, value="Prompt", label="Prompt"
                )

                image2image_negative_prompt = gr.Textbox(
                    lines=1,
                    value="Negative Prompt",
                    label="Negative Prompt",
                )

                with gr.Accordion("Advanced Options", open=False):
                    image2image_guidance_scale = gr.Slider(
                        minimum=0.1,
                        maximum=15,
                        step=0.1,
                        value=7.5,
                        label="Guidance Scale",
                    )

                    image2image_num_inference_step = gr.Slider(
                        minimum=1,
                        maximum=100,
                        step=1,
                        value=50,
                        label="Num Inference Step",
                    )

                image2image_predict = gr.Button(value="Generator")

            with gr.Column():
                output_image = gr.Image(label="Output")

        image2image_predict.click(
            fn=stable_diffusion_img2img,
            inputs=[
                image2image2_image_file,
                image2image_model_path,
                image2image_prompt,
                image2image_negative_prompt,
                image2image_guidance_scale,
                image2image_num_inference_step,
            ],
            outputs=[output_image],
        )

import gradio as gr
import torch
from controlnet_aux import HEDdetector
from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler,
)
from PIL import Image

from diffusion_webui.utils.model_list import (
    controlnet_hed_model_list,
    stable_model_list,
)


def controlnet_hed(image_path: str, controlnet_hed_model_path: str):
    hed = HEDdetector.from_pretrained("lllyasviel/ControlNet")

    image = Image.open(image_path)
    image = hed(image)

    controlnet = ControlNetModel.from_pretrained(
        controlnet_hed_model_path, torch_dtype=torch.float16
    )
    return controlnet, image


def stable_diffusion_controlnet_hed(
    image_path: str,
    stable_model_path: str,
    controlnet_hed_model_path: str,
    prompt: str,
    negative_prompt: str,
    num_images_per_prompt: int,
    guidance_scale: int,
    num_inference_step: int,
):

    controlnet, image = controlnet_hed(
        image_path=image_path,
        controlnet_hed_model_path=controlnet_hed_model_path,
    )

    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        pretrained_model_name_or_path=stable_model_path,
        controlnet=controlnet,
        safety_checker=None,
        torch_dtype=torch.float16,
    )

    pipe.to("cuda")
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_xformers_memory_efficient_attention()

    output = pipe(
        prompt=prompt,
        image=image,
        negative_prompt=negative_prompt,
        num_images_per_prompt=num_images_per_prompt,
        num_inference_steps=num_inference_step,
        guidance_scale=guidance_scale,
    ).images

    return output


def stable_diffusion_controlnet_hed_app():
    with gr.Blocks():
        with gr.Row():
            with gr.Column():
                controlnet_hed_image_file = gr.Image(
                    type="filepath", label="Image"
                )

                controlnet_hed_stable_model_id = gr.Dropdown(
                    choices=stable_model_list,
                    value=stable_model_list[0],
                    label="Stable Model Id",
                )

                controlnet_hed_model_id = gr.Dropdown(
                    choices=controlnet_hed_model_list,
                    value=controlnet_hed_model_list[0],
                    label="ControlNet Model Id",
                )

                controlnet_hed_prompt = gr.Textbox(
                    lines=1, value="Prompt", label="Prompt"
                )

                controlnet_hed_negative_prompt = gr.Textbox(
                    lines=1,
                    value="Negative Prompt",
                    label="Negative Prompt",
                )

                controlnet_hed_num_images_per_prompt = gr.Slider(
                    minimum=1,
                    maximum=10,
                    step=1,
                    value=1,
                    label="Number Of Images",
                )
                with gr.Accordion("Advanced Options", open=False):
                    controlnet_hed_guidance_scale = gr.Slider(
                        minimum=0.1,
                        maximum=15,
                        step=0.1,
                        value=7.5,
                        label="Guidance Scale",
                    )

                    controlnet_hed_num_inference_step = gr.Slider(
                        minimum=1,
                        maximum=100,
                        step=1,
                        value=50,
                        label="Num Inference Step",
                    )

                controlnet_hed_predict = gr.Button(value="Generator")

            with gr.Column():
                output_image = gr.Gallery(
                    label="Generated images",
                    show_label=False,
                    elem_id="gallery",
                ).style(grid=(1, 2))

        controlnet_hed_predict.click(
            fn=stable_diffusion_controlnet_hed,
            inputs=[
                controlnet_hed_image_file,
                controlnet_hed_stable_model_id,
                controlnet_hed_model_id,
                controlnet_hed_prompt,
                controlnet_hed_negative_prompt,
                controlnet_hed_num_images_per_prompt,
                controlnet_hed_guidance_scale,
                controlnet_hed_num_inference_step,
            ],
            outputs=[output_image],
        )

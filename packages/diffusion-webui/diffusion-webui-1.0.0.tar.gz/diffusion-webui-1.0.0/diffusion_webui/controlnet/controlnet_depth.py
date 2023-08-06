import gradio as gr
import numpy as np
import torch
from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler,
)
from PIL import Image
from transformers import pipeline

from diffusion_webui.utils.model_list import (
    controlnet_depth_model_list,
    stable_model_list,
)


def controlnet_depth(image_path: str, depth_model_path: str):
    depth_estimator = pipeline("depth-estimation")

    image = Image.open(image_path)
    image = depth_estimator(image)["depth"]
    image = np.array(image)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    image = Image.fromarray(image)

    controlnet = ControlNetModel.from_pretrained(
        depth_model_path, torch_dtype=torch.float16
    )

    return controlnet, image


def stable_diffusion_controlnet_depth(
    image_path: str,
    stable_model_path: str,
    depth_model_path: str,
    prompt: str,
    negative_prompt: str,
    num_images_per_prompt: int,
    guidance_scale: int,
    num_inference_step: int,
):

    controlnet, image = controlnet_depth(
        image_path=image_path, depth_model_path=depth_model_path
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


def stable_diffusion_controlnet_depth_app():
    with gr.Blocks():
        with gr.Row():
            with gr.Column():
                controlnet_depth_image_file = gr.Image(
                    type="filepath", label="Image"
                )

                controlnet_depth_stable_model_id = gr.Dropdown(
                    choices=stable_model_list,
                    value=stable_model_list[0],
                    label="Stable Model Id",
                )

                controlnet_depth_model_id = gr.Dropdown(
                    choices=controlnet_depth_model_list,
                    value=controlnet_depth_model_list[0],
                    label="ControlNet Model Id",
                )

                controlnet_depth_prompt = gr.Textbox(
                    lines=1, value="Prompt", label="Prompt"
                )

                controlnet_depth_negative_prompt = gr.Textbox(
                    lines=1,
                    value="Negative Prompt",
                    label="Negative Prompt",
                )

                controlnet_depth_num_images_per_prompt = gr.Slider(
                    minimum=1,
                    maximum=10,
                    step=1,
                    value=1,
                    label="Number Of Images",
                )
                with gr.Accordion("Advanced Options", open=False):
                    controlnet_depth_guidance_scale = gr.Slider(
                        minimum=0.1,
                        maximum=15,
                        step=0.1,
                        value=7.5,
                        label="Guidance Scale",
                    )

                    controlnet_depth_num_inference_step = gr.Slider(
                        minimum=1,
                        maximum=100,
                        step=1,
                        value=50,
                        label="Num Inference Step",
                    )

                controlnet_depth_predict = gr.Button(value="Generator")

            with gr.Column():
                output_image = gr.Gallery(
                    label="Generated images",
                    show_label=False,
                    elem_id="gallery",
                ).style(grid=(1, 2))

        controlnet_depth_predict.click(
            fn=stable_diffusion_controlnet_depth,
            inputs=[
                controlnet_depth_image_file,
                controlnet_depth_stable_model_id,
                controlnet_depth_model_id,
                controlnet_depth_prompt,
                controlnet_depth_negative_prompt,
                controlnet_depth_num_images_per_prompt,
                controlnet_depth_guidance_scale,
                controlnet_depth_num_inference_step,
            ],
            outputs=output_image,
        )

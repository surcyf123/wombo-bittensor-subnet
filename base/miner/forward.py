import pickle

from base.protocol import ImageGenerationSynapse

import torch
from diffusers.pipelines.stable_diffusion_xl.pipeline_stable_diffusion_xl import StableDiffusionXLPipeline


class SDXLMinerPipeline(StableDiffusionXLPipeline):
    def generate(self, **inputs):
        frames = []
        inputs["generator"] = torch.Generator().manual_seed(inputs["seed"])

        def save_frames(pipe, step_index, timestep, callback_kwargs):
            frames.append(callback_kwargs["latents"])
            return callback_kwargs

        images = self(
            **inputs,
            callback_on_step_end=save_frames,
        )
        frames_tensor = torch.stack(frames)
        return frames_tensor, images


def forward(self, request: ImageGenerationSynapse):
    request.output_data = pickle.dumps(self.pipeline.generate(**request.input_parameters))
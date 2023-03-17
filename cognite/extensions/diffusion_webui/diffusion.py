import asyncio
import aiohttp
import requests
from PIL import Image, ImageDraw
import io
import base64

async def post_request(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()
            
class DiffusionExtension:
    def __init__(self, url) -> None:
        self.url = url
        
    def get_payload(self, prompt: str, negative_prompt: str, steps: int, cfg_scale: float, width: int, height: int, sampler: str):
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            "sampler_index": sampler,
        }
        return payload
        
    def diffusion_wrapper(self, prompt: str, negative_prompt: str, steps: int, cfg_scale: float, width: int, height: int, sampler: str):
        payload = self.get_payload(prompt, negative_prompt, steps, cfg_scale, width, height, sampler)
        response = requests.post(url=f'{self.url}/sdapi/v1/txt2img', json=payload)
        r = response.json()
        images = []
        if 'images' in r:
            for image in r['images']:
                images.append(Image.open(io.BytesIO(base64.b64decode(image.split(",",1)[0]))))
        else:
            raise Exception("No images in response")
        return image
            
    async def async_diffusion_wrapper(self, prompt: str, negative_prompt: str, steps: int, cfg_scale: float, width: int, height: int, sampler: str):
        payload = self.get_payload(prompt, negative_prompt, steps, cfg_scale, width, height, sampler)
        response = await post_request(self.url, payload)
        r = response.json()
        images = []
        if 'images' in r:
            for image in r['images']:
                images.append(Image.open(io.BytesIO(base64.b64decode(image.split(",",1)[0]))))
        else:
            raise Exception("No images in response")
        return image
    
    def ask_diffusion(self, prompt: str, negative_prompt: str, steps: int, cfg_scale: float, width: int, height: int, sampler: str, use_async=False):
        if use_async:
            rloop = asyncio.get_event_loop()
            return rloop.run_until_complete(self.async_diffusion_wrapper(prompt, negative_prompt, steps, cfg_scale, width, height, sampler))
        else:
            return self.diffusion_wrapper(prompt, negative_prompt, steps, cfg_scale, width, height, sampler)
        
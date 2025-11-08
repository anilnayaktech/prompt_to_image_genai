# scripts/image_pipeline.py

import os
import torch
from datetime import datetime
from diffusers import StableDiffusionPipeline
from transformers import pipeline as hf_pipeline
from scripts.safety import is_safe_prompt  # safety check (create this small file)

# ---------------------------------------
# Step 1: Optional - Use an LLM to refine the prompt
# ---------------------------------------

# Load a lightweight text2text model (for creative prompt enhancement)
prompt_refiner = hf_pipeline("text2text-generation", model="google/flan-t5-small")

def refine_prompt(user_prompt: str) -> str:
    """
    Uses a small LLM to make user prompts more creative and detailed.
    """
    refined = prompt_refiner(
        f"Make this image prompt more descriptive and imaginative: {user_prompt}",
        max_new_tokens=40
    )[0]['generated_text']
    return refined


# ---------------------------------------
# Step 2: Load Stable Diffusion Model (only once)
# ---------------------------------------

model_id = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Stable Diffusion model
print("🔄 Loading Stable Diffusion model... (first time may take a minute)")
image_generator = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to(device)


# ---------------------------------------
# Step 3: Generate Image + Save to Folder
# ---------------------------------------

def generate_image(prompt: str, enhance_prompt: bool = True):
    """
    Generates an AI image from a text prompt.
    Optionally enhances the prompt using an LLM first.
    Saves the image into data/samples/ and returns the image + prompt.
    """

    # ✅ Safety filter
    if not is_safe_prompt(prompt):
        raise ValueError("🚫 Unsafe or inappropriate content detected in the prompt!")

    # ✅ Refine prompt if user selected "Enhance"
    if enhance_prompt:
        prompt = refine_prompt(prompt)

    # ✅ Generate image
    print("🎨 Generating image...")
    result = image_generator(prompt, num_inference_steps=30, guidance_scale=7.5)
    image = result.images[0]

    # ✅ Create folder if not exists
    save_dir = os.path.join("data", "samples")
    os.makedirs(save_dir, exist_ok=True)

    # ✅ Save with unique filename
    safe_name = "_".join(prompt.split()[:5])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp}.png"
    save_path = os.path.join(save_dir, filename)
    image.save(save_path)

    print(f"✅ Image saved at: {save_path}")
    return image, prompt, save_path

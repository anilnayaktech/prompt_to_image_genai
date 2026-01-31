# scripts/image_pipeline.py

import os
import glob
import torch
from datetime import datetime
from diffusers import StableDiffusionPipeline
from transformers import pipeline as hf_pipeline
from scripts.safety import is_safe_prompt  # safety check (create this small file)

# ---------------------------------------
# Step 1: Optional - Use an LLM to refine the prompt
# ---------------------------------------

print("Initializing prompt refiner (Flan-T5-small)...")
# Load a lightweight text2text model (for creative prompt enhancement)
prompt_refiner = hf_pipeline("text-generation", model="google/flan-t5-small")
print("Prompt refiner loaded successfully.")

def refine_prompt(user_prompt: str) -> str:
    """
    Uses a small LLM to make user prompts more creative and detailed.
    Adds fallback checks to avoid nonsense outputs.
    """
    print(f"Refining user prompt: {user_prompt}")
    # Skip refinement if the prompt is too short 
    if len(user_prompt.split()) < 3: 
        print("Prompt too short, skipping refinement.")
        return user_prompt
   # refined = prompt_refiner(f"Make this image prompt more descriptive and imaginative: {user_prompt}",max_new_tokens=40 )[0]['generated_text']
    refined = prompt_refiner( f"Rewrite this as a vivid artistic scene description: {user_prompt}", max_new_tokens=40 )[0]['generated_text']
    if not refined or refined.strip() == "" or refined.lower().startswith("a picture of a man") or refined.count(" ") < 3: 
        print("Refinement produced poor output, falling back to original prompt.") 
        return user_prompt
    
    print(f"Refined prompt: {refined}")
    return refined


# ---------------------------------------
# Step 2: Load Stable Diffusion Model (only once)
# ---------------------------------------

model_id = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device selected: {device}")
# Load Stable Diffusion model
print("Loading Stable Diffusion model... (first time may take a minute)")
image_generator = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to(device)
print("Stable Diffusion model loaded successfully.")


# ---------------------------------------
# Step 3: Generate Image + Save to Folder
# ---------------------------------------

def generate_image(prompt: str, enhance_prompt: bool = True):
    clear_samples_folder() # <-- cleanup step
    """
    Generates an AI image from a text prompt.
    Optionally enhances the prompt using an LLM first.
    Saves the image into data/samples/ and returns the image + prompt.
    """

    print("Starting image generation pipeline...")
    print(f"Original prompt: {prompt}")
    print(f"Enhance prompt option: {enhance_prompt}")

    #  Safety filter
    if not is_safe_prompt(prompt):
        print("Unsafe prompt detected. Aborting image generation.")
        raise ValueError("Unsafe or inappropriate content detected in the prompt!")
    else:
        print("Prompt passed safety check.")

    #  Refine prompt if user selected "Enhance"
    if enhance_prompt:
        prompt = refine_prompt(prompt)
    else:
        print("Prompt enhancement skipped.")

    # Generate image
    print("🎨 Generating image with Stable Diffusion...")
    result = image_generator(prompt, num_inference_steps=30, guidance_scale=7.5)
    image = result.images[0]
    print("Image generation complete.")

    #  Create folder if not exists
    save_dir = os.path.join("data", "samples")
    if not os.path.exists(save_dir):
        print(f"Creating directory: {save_dir}")
    os.makedirs(save_dir, exist_ok=True)

    # Save with unique filename
    safe_name = "_".join(prompt.split()[:5])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp}.png"
    save_path = os.path.join(save_dir, filename)
    image.save(save_path)

    print(f"Image saved successfully at: {save_path}")
    print("Returning image object, refined prompt, and save path.")

    return image, prompt, save_path


def clear_samples_folder():
    """
    Deletes all .png files inside data/samples/ before generating new images.
    """
    folder = os.path.join("data", "samples")
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")
        return

    files = glob.glob(os.path.join(folder, "*.png"))
    for f in files:
        try:
            os.remove(f)
            print(f"Deleted: {f}")
        except Exception as e:
            print(f"Could not delete {f}: {e}")
    print("Cleared all .png files from data/samples/")
 
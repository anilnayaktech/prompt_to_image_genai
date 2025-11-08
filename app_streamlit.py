# app_streamlit.py

import streamlit as st
from scripts.image_pipeline import generate_image

# ---------------------------------------
# Streamlit UI Setup
# ---------------------------------------
st.set_page_config(page_title="Prompt-to-Image Generator", layout="wide")

st.title("🎨 GenAI Prompt-to-Image Generator")
st.write("Type a creative prompt below and watch AI turn your words into art!")

# ---------------------------------------
# User Input
# ---------------------------------------
prompt = st.text_area("Enter your image prompt:", placeholder="e.g., A castle floating in the clouds during sunset")

enhance = st.checkbox("✨ Enhance my prompt using AI", value=True)

if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        try:
            with st.spinner("🪄 Creating your image... please wait..."):
                image, refined_prompt, image_path = generate_image(prompt, enhance_prompt=enhance)
            st.image(image, caption=f"🖼️ Prompt used: {refined_prompt}", width=256)
            st.success(f"✅ Image saved at: {image_path}")
        except Exception as e:
            st.error(f"Error: {e}")

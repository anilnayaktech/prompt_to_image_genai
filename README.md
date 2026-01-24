# 🎨 GenAI Prompt-to-Image Generator

A simple **Generative AI web app** built with **Streamlit**, **Hugging Face Transformers**, and **Stable Diffusion**, where users can type any text prompt and generate beautiful AI art instantly.  
It also includes **prompt enhancement** using a lightweight LLM and **safe-content filtering**.

---

## 🚀 Features
- 🧠 LLM-powered prompt enhancement (using `flan-t5-small`)
- 🎨 Image generation with `Stable Diffusion v1-5`
- 🛡️ Basic NSFW / unsafe prompt filtering
- 💾 Auto-save generated images in `data/samples/`
- 🌐 Streamlit UI for easy interaction

---

## 🧰 Project Structure
...
genai_prompt2image/
│
├── app_streamlit.py # Streamlit frontend app
├── scripts/
│ ├── image_pipeline.py # Main text→image logic
│ ├── safety.py # Prompt safety filtering
│
├── data/
│ └── samples/ # Stores generated images
│
├── requirements.txt # Python dependencies
└── README.md # Documentation
...

---

## ⚙️ Setup Instructions

### 1️⃣ Create & Activate Virtual Environment
```bash
python -m venv genai_env

# Activate it:
# On Windows:
genai_env\Scripts\activate

# On Mac/Linux:
source genai_env/bin/activate
2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Run the Streamlit App
bash
Copy code
streamlit run app_streamlit.py
💡 Example Prompts
Try these fun prompts:

"A fantasy castle above the clouds at sunset"

"A futuristic robot painting a landscape"

📂 Output
Generated images will be automatically saved in:

bash
Copy code
data/samples/
🧠 Tech Stack
Python

Streamlit

Hugging Face Transformers

Diffusers (Stable Diffusion)

Torch

👩‍💻 Author
Anil Kumar Nayak
✨ Software Developer | Python, AI & Streamlit Enthusiast
📧 anilnayak.tech@gmail.com

🏁 Future Enhancements
Add multiple image styles (e.g., anime, photorealistic)

Add download/share button

Integrate OpenAI API for higher-quality prompt generation

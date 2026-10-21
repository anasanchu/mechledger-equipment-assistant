# MinerU Gradio UI Deployment

This folder contains a standalone, beautiful Gradio UI designed specifically for deploying MinerU on Hugging Face Spaces (or locally) without the need for complex Dockerfiles.

## Features
- **Unlimited Pages:** Bypass standard page limits natively by exposing an unlocked slider (up to 5000+ pages).
- **Custom UI:** A dark-mode, glassmorphic UI built natively with Gradio Blocks.
- **Model Selection:** Ability to dynamically toggle OCR and choose layout models (e.g. LayoutLMv3).
- **Direct Downloads:** Extracts the PDF and instantly provides download links for the Markdown and JSON structured data.

## How to deploy on Hugging Face Spaces:
1. Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2. Choose **Gradio** as the Space SDK (do NOT choose Docker).
3. Upload the three files in this folder (`app.py`, `requirements.txt`, `packages.txt`) to the root of your new Space repository.
4. Hugging Face will automatically read `packages.txt` to install the OpenCV C++ dependencies, read `requirements.txt` to install MinerU/Gradio, and then launch `app.py`.

*Note: The very first time you parse a document, MinerU will download the required `pdf-extract-kit` weights in the background.*

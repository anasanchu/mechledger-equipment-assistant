FROM python:3.10-slim

# Install necessary system dependencies for OpenCV and layout rendering
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev wget curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Gradio, MinerU and PyMuPDF globally
RUN pip install --no-cache-dir --upgrade pip uv
RUN uv pip install --system -U "mineru[all]>=3.4.0" gradio>=4.0.0 pymupdf huggingface_hub

# Set Hugging Face specific environment variables
ENV MINERU_BACKEND="pipeline"
ENV PYTHONUNBUFFERED=1

# Create non-root user and ensure /data has correct permissions
RUN useradd -m -u 1000 user && \
    mkdir -p /data && \
    chown -R user:user /data

# HF_HOME tells Hugging Face Hub (and MinerU) where to store downloaded models
ENV HF_HOME="/data"

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy the custom Gradio UI script into the container
COPY --chown=user app.py $HOME/app/app.py

EXPOSE 7860

# We cannot pre-bake the models during the build phase (causes 'unable to schedule' 
# due to 15GB+ image size on HF Free Tier). 
# Instead, we download them dynamically every time the container wakes up.
CMD ["/bin/bash", "-c", "mineru-models-download -s huggingface -m all && python app.py"]

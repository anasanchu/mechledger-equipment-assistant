import gradio as gr
from sentence_transformers import SentenceTransformer
import json
import os
import torch
import torch.nn.functional as F

# Load the nomic model. Nomic models require trust_remote_code=True
print("Loading nomic-ai/nomic-embed-text-v1.5 model...")
# Note: nomic-embed-text-v1.5 produces 768-dimensional embeddings by default.
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
print("Model loaded successfully!")

def generate_embeddings(texts_json):
    """
    Accepts a JSON string of a list of texts.
    Returns a JSON string of a list of embedding vectors.
    """
    try:
        texts = json.loads(texts_json)
        if not isinstance(texts, list):
            return json.dumps({"error": "Input must be a JSON list of strings."})
            
        # Add prefix for document embedding as recommended by Nomic
        # "search_document: " is typically used for documents being stored in a DB
        prefixed_texts = ["search_document: " + t for t in texts]
        
        # Encode
        embeddings = model.encode(prefixed_texts, convert_to_tensor=True)
        
        # We output the full 768-dimensional vectors since you are creating a new cluster
        embeddings = F.normalize(embeddings, p=2, dim=1)
        
        return json.dumps(embeddings.tolist())
    except Exception as e:
        return json.dumps({"error": str(e)})

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🧠 IKB-RAG Nomic Embeddings API")
    gr.Markdown("This space securely serves the `nomic-ai/nomic-embed-text-v1.5` model for the IKB-RAG application.")
    
    with gr.Row():
        input_text = gr.Textbox(lines=5, label="Input JSON (List of strings)", placeholder='["What is a pump?", "How to fix a valve."]')
        output_text = gr.Textbox(lines=5, label="Output JSON (Embeddings)")
        
    btn = gr.Button("Generate Vectors", variant="primary")
    btn.click(fn=generate_embeddings, inputs=input_text, outputs=output_text, api_name="generate_embeddings")

# Queue is required for spaces handling multiple concurrent API requests
demo.queue()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)

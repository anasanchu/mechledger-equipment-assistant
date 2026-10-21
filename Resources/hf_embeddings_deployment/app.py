import gradio as gr
import json
from sentence_transformers import SentenceTransformer

print("Loading Embedding Model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Model loaded.")

def generate_embeddings(text_chunks_json):
    """Takes a JSON string of text chunks and returns a JSON string of embeddings."""
    try:
        chunks = json.loads(text_chunks_json)
        # Generate mathematical embeddings
        embeddings = model.encode(chunks).tolist()
        return json.dumps(embeddings)
    except Exception as e:
        return json.dumps({"error": str(e)})

iface = gr.Interface(
    fn=generate_embeddings,
    inputs=gr.Textbox(label="JSON List of Texts"),
    outputs=gr.Textbox(label="JSON List of Embeddings")
)
iface.launch()

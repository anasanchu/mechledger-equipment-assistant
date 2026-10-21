import gradio as gr
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch

print("Loading model... this takes a minute on startup.")

# We use Qwen2-VL-2B because it is natively supported by transformers (no trust_remote_code needed!)
# and fits within the 16GB RAM limit of Hugging Face's Free CPU tier.
model_id = "Qwen/Qwen2-VL-2B-Instruct"

# Load the model directly without trust_remote_code
model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_id, torch_dtype="auto", device_map="cpu"
)

# default processer
processor = AutoProcessor.from_pretrained(model_id)

def analyze_pid(image_path, prompt):
    if not image_path:
        return "No image provided."
    if not prompt:
        prompt = "Extract all text, equipment tags, and describe connections in this diagram."
        
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image_path,
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        # Preparation for inference
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )

        # Inference: Generation of the output
        generated_ids = model.generate(**inputs, max_new_tokens=256)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        return output_text[0]
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

# The Gradio Interface automatically creates an API endpoint!
iface = gr.Interface(
    fn=analyze_pid,
    inputs=[
        gr.Image(type="filepath", label="Upload P&ID"), 
        gr.Textbox(label="Prompt", placeholder="What do you want to extract?")
    ],
    outputs=gr.Textbox(label="Vision Analysis"),
    title="IKB Custom Vision Agent",
    description="This is a dedicated multimodal API for extracting knowledge from industrial P&IDs."
)

iface.launch()

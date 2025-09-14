from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch
import gradio as gr
from gtts import gTTS
import os

# -------------------
# Load models
# -------------------
# Translation model (NLLB-200)
nllb_model_name = "facebook/nllb-200-distilled-600M"
nllb_tokenizer = AutoTokenizer.from_pretrained(nllb_model_name)
nllb_model = AutoModelForSeq2SeqLM.from_pretrained(nllb_model_name)

# Chat model (GPT-OSS-20B)
chat_model_name = "openai/gpt-oss-20b"
chat_tokenizer = AutoTokenizer.from_pretrained(chat_model_name)
chat_model = AutoModelForCausalLM.from_pretrained(
    chat_model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

# -------------------
# Translation function
# -------------------
def translate(text, src_lang, tgt_lang):
    nllb_tokenizer.src_lang = src_lang
    inputs = nllb_tokenizer(text, return_tensors="pt")
    translated_tokens = nllb_model.generate(
        **inputs,
        forced_bos_token_id=nllb_tokenizer.lang_code_to_id[tgt_lang]
    )
    return nllb_tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

# -------------------
# Chat function (GPT-OSS)
# -------------------
def chat_with_bot(user_input, history=[]):
    history.append({"role": "user", "content": user_input})

    inputs = chat_tokenizer.apply_chat_template(
        history,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt"
    ).to(chat_model.device)

    outputs = chat_model.generate(
        **inputs,
        max_new_tokens=120,
        do_sample=True,
        top_p=0.9,
        temperature=0.7
    )
    response = chat_tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True
    )

    history.append({"role": "assistant", "content": response})
    return response, history

# -------------------
# Combined chatbot logic
# -------------------
def main_chat(user_input, history, mode, direction):
    if mode == "Translation":
        if direction == "English → Yoruba":
            response = translate(user_input, "eng_Latn", "yor_Latn")
        else:
            response = translate(user_input, "yor_Latn", "eng_Latn")
    else:  # Chat Mode
        response, history = chat_with_bot(user_input, history)

    history.append((user_input, response))
    return history, history, tts_output(response)

# -------------------
# Text-to-Speech
# -------------------
def tts_output(text, lang="en"):
    if any(ch in text for ch in "ẹọṣáíóú"):  # crude check for Yoruba letters
        lang = "yo"
    tts = gTTS(text=text, lang=lang)
    filename = "response.mp3"
    tts.save(filename)
    return filename

# -------------------
# Gradio UI
# -------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🗣️ Yoruba Machine Translation & Chatbot")

    with gr.Row():
        mode = gr.Radio(["Chat", "Translation"], label="Select Mode", value="Translation")
        direction = gr.Radio(["English → Yoruba", "Yoruba → English"], label="Translation Direction", value="English → Yoruba")

    chatbot_ui = gr.Chatbot(label="Chat History")
    msg = gr.Textbox(label="Type or speak...", placeholder="Enter your message...")
    clear = gr.Button("Clear History")

    with gr.Row():
        voice_in = gr.Audio(source="microphone", type="filepath", label="🎤 Speak")
        tts_out = gr.Audio(label="🔊 Bot Voice", type="filepath")

    # Connect functions
    msg.submit(main_chat, [msg, chatbot_ui, mode, direction], [chatbot_ui, chatbot_ui, tts_out])
    clear.click(lambda: None, None, chatbot_ui, queue=False)

demo.launch()

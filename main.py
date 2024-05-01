import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import os 
import PIL

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# List available models
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

# Generate text from text inputs
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("What is the meaning of life?")
to_markdown(response.text)

# Generate text from image and text inputs
img_path = 'image.jpg'
img = PIL.Image.open(img_path)
model = genai.GenerativeModel('gemini-pro-vision')
response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img], stream=True)
response.resolve()
to_markdown(response.text)

# Chat conversations
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
response = chat.send_message("In one sentence, explain how a computer works to a young child.")
to_markdown(response.text)

# Count tokens
model = genai.GenerativeModel('gemini-pro')
token_count = model.count_tokens("What is the meaning of life?")
print(token_count)

# Use embeddings
result = genai.embed_content(
    model="models/embedding-001",
    content="What is the meaning of life?",
    task_type="retrieval_document",
    title="Embedding of single string")
print(result['embedding'])

# Advanced use cases
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('[Questionable prompt here]')
print(response.candidates)
print(response.prompt_feedback)
response = model.generate_content('[Questionable prompt here]',
                                  safety_settings={'HARASSMENT':'block_none'})
print(response.text)

# Encode messages
model = genai.GenerativeModel('gemini-pro-vision')
messages = [
    {'role':'user',
     'parts': ["Briefly explain how a computer works to a young child."]}
]
response = model.generate_content(messages)
to_markdown(response.text)

# Multi-turn conversations
messages = [
    {'role':'user',
     'parts': ["Briefly explain how a computer works to a young child."]}
]
response = model.generate_content(messages)
messages.append({'role':'model', 'parts':[response.text]})
messages.append({'role':'user', 'parts':["Okay, how about a more detailed explanation to a high school student?"]})
response = model.generate_content(messages)
to_markdown(response.text)

# Generation configuration
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(
    'Tell me a story about a magic backpack.',
    generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        stop_sequences=['x'],
        max_output_tokens=20,
        temperature=1.0)
)
text = response.text
if response.candidates[0].finish_reason.name == "MAX_TOKENS":
    text += '...'
to_markdown(text)
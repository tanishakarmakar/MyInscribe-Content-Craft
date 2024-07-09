from transformers import pipeline
import spacy
from textstat import textstat
from collections import Counter
import re
import language_tool_python
from llama_cpp import Llama
import os

# Path to the model directory
model_dir = './models/7B/'

# List all files in the directory
files = os.listdir(model_dir)
print("Files in the directory:", files)

# Assuming the correct file name is the one with the suffix
correct_model_path = None
for file in files:
    if file.startswith("llama-2-7b-chat.Q4_K_M.gguf"):
        correct_model_path = os.path.join(model_dir, file)
        break

if correct_model_path is None:
    raise ValueError("Model file not found in the directory.")

print(f"Using model file: {correct_model_path}")

# Initialize Llama model
llm = Llama(
    model_path=correct_model_path,
    n_gpu_layers=50
)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize transformers pipeline for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

def generate_content(prompt, max_tokens=512, chunk_size=100, stop_sequences=["\n"], context_window=512):
    # Initialize response text and token counters
    response_text = ""
    total_tokens = 0
    prompt_tokens = len(prompt.split())

    # Prepare the prompt by adding "Q:" at the beginning and "A:" at the end
    formatted_prompt = f"Q: {prompt}\nA:"

    # Truncate the prompt if it exceeds the context window
    if prompt_tokens >= context_window:
        prompt_tokens = context_window - 1
        formatted_prompt = ' '.join(formatted_prompt.split()[:prompt_tokens])

    max_tokens = min(max_tokens, context_window - prompt_tokens)

    while total_tokens < max_tokens:
        available_tokens = context_window - prompt_tokens - total_tokens
        if available_tokens <= 0:
            break

        current_chunk_size = min(chunk_size, available_tokens)

        # Generate a response chunk using the formatted prompt
        response = llm(
            formatted_prompt + response_text,
            max_tokens=current_chunk_size,
            stop=stop_sequences
        )

        chunk = response['choices'][0]['text'].strip()
        chunk_tokens = len(chunk.split())
        total_tokens += chunk_tokens

        if total_tokens >= max_tokens:
            last_period_index = chunk.rfind('.')
            if last_period_index != -1:
                chunk = chunk[:last_period_index + 1]
            else:
                chunk = chunk.rstrip('.!?,')
        
        response_text += " " + chunk

        if response_text.strip()[-1] in ['.', '!', '?']:
            break

    return response_text.strip()


def optimize_content(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def analyze_content(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {"entities": entities}

def get_readability_score(text):
    return textstat.flesch_reading_ease(text)

def keyword_density_analysis(text):
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    keyword_counts = Counter(words)
    keyword_density = {word: count / total_words * 100 for word, count in keyword_counts.items()}
    return keyword_density

def grammar_and_spelling_check(text):
    matches = tool.check(text)
    corrections = [{'message': match.message, 'corrections': match.replacements} for match in matches]
    return corrections

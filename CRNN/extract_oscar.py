from datasets import load_dataset
from huggingface_hub import login
import os
import re
import logging

# Configure logging
logging.basicConfig(filename='oscar_extract.log', level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
token = "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"  # Your token
login(token=token)

def clean_text(text, lang):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    if lang == 'hi':
        text = re.sub(r'[^\s\u0900-\u097F]', '', text)  # Hindi
    elif lang == 'zh':
        text = re.sub(r'[^\s\u4E00-\u9FFF]', '', text)  # Chinese
    elif lang == 'ar':
        text = re.sub(r'[^\s\u0600-\u06FF]', '', text)  # Arabic
    else:
        text = re.sub(r'[^\w\s]', '', text)  # English, Spanish
    return text.strip()

def split_into_words(text):
    return [word for word in text.split() if 1 <= len(word) <= 15]  # Words 1–15 chars

languages = ['en', 'es', 'hi', 'zh', 'ar']
os.makedirs('C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/oscar', exist_ok=True)
for lang in languages:
    dataset = load_dataset(
        "oscar-corpus/OSCAR-2301",
        language=lang,
        split="train",
        streaming=True,
        token=token,
        trust_remote_code=True
    )
    output_path = f'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/oscar/oscar_{lang}_clean.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        count = 0
        for i, item in enumerate(dataset):
            if i >= 50000:  # Increase to 50000 samples
                break
            text = item['text'].strip()
            cleaned = clean_text(text, lang)
            words = split_into_words(cleaned)
            for word in words:
                f.write(word + '\n')
                count += 1
            if i % 1000 == 0:  # Log every 1000 samples
                logger.info(f"[{lang}] Sample {i}: Raw: {text[:100]} | Cleaned: {cleaned[:100]} | Words: {words[:5]}")
        logger.info(f"[{lang}] Total written: {count} lines")
    print(f"[{lang}] Written {count} lines to {output_path}")
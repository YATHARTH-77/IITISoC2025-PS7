from datasets import load_dataset
from huggingface_hub import login
import os
import re
import logging

# Configure logging
logging.basicConfig(filename='oscar_extract_debug.log', level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
token = "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"  # Your token
login(token=token)

def clean_text(text, lang):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    if lang in ['hi', 'zh', 'ar']:
        text = re.sub(r'[^\s\u0900-\u097F\u4E00-\u9FFF\u0600-\u06FF]', '', text)  # Keep Hindi, Chinese, Arabic
    else:
        text = re.sub(r'[^\w\s]', '', text)  # Keep alphanumeric for en, es
    return text.strip()

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
    with open(f'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/oscar/oscar_{lang}_clean.txt', 'w', encoding='utf-8') as f:
        count = 0
        for i, item in enumerate(dataset):
            if i >= 10000:  # Increase to 10000 samples
                break
            text = item['text'].strip()
            logger.info(f"[{lang}] Raw {i}: {text[:100]}")
            cleaned = clean_text(text, lang)
            logger.info(f"[{lang}] Cleaned {i}: {cleaned[:100]}")
            if cleaned and 1 <= len(cleaned) <= 30:  # Relax length to 30
                f.write(cleaned + '\n')
                count += 1
        logger.info(f"[{lang}] Total written: {count} lines")
    print(f"[{lang}] Written {count} lines to oscar_{lang}_clean.txt")
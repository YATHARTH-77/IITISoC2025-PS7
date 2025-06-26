from datasets import load_dataset
from huggingface_hub import login
import os

# Suppress symlinks warning
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Authenticate
token = "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"  # Your valid token
login(token=token)

# Test access
try:
    dataset = load_dataset(
        "oscar-corpus/OSCAR-2301",
        language="en",
        split="train",
        streaming=True,
        token=token,
        trust_remote_code=True
    )
    for i, d in enumerate(dataset):
        if i >= 1000:  # Limit to 1000 samples
            break
        print(d['text'][:100])
        if i < 3:  # Print first 3 for verification
            print(f"Sample {i+1}: {d['text'][:100]}")
except Exception as e:
    print(f"Error: {e}")
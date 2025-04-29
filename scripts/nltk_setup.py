import nltk
import os

def ensure_nltk_resources():
    """
    Check and download required NLTK resources if missing.
    """
    required_packages = ['punkt', 'punkt_tab']

    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            print(f"Downloading missing NLTK resource: {package}...")
            nltk.download(package)

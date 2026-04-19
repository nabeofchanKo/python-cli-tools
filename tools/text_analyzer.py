import re
from collections import Counter
import argparse

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "shall",
    "can", "it", "its", "this", "that", "these", "those", "i",
    "me", "my", "we", "our", "you", "your", "he", "she", "they",
}

def load_text(filepath:str) -> str:
    with open(filepath, "r") as f:
        text = f.read()
    
    return text

def count_chars(text:str) -> tuple:
    return (len(text), len(text.replace(" ", "")))

def count_words(text:str) -> int:
    return len(text.split())

def count_lines(text:str) -> int:
    return len(text.splitlines())

def get_top_words(text:str, n:int) -> list:
    words = text.lower().split()
    
    filtered = []
    for word in words:
        word = word.strip(".,;:!?()")
        if word not in STOP_WORDS:
            filtered.append(word)

    return Counter(filtered).most_common(n)

def extract_emails(text:str) -> list:
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_urls(text:str) -> list:
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)

def display_results(text:str) -> None:

    if text:
        print("=== Results of Text Analysis ===")

        charts = count_chars(text)
        print(f'1. Characters Count: {charts[0]} characters (with spaces) / {charts[1]} characters (without spaces)')
        
        print(f'2. Words Count: {count_words(text)} words')

        print(f'3. Lines Count: {count_lines(text)} lines')

        print(f'4. Top 15 Words in Text (Excluding Stop Words):')
        rank = 1

        for word in get_top_words(text, 15):
            print(f'Top {rank}: {word[0]} / {word[1]} times')
            rank += 1
            
        print(f'5. E-mail Address in Text:')
        for address in extract_emails(text):
            print(f" - {address}")

        print(f'6. URL in Text:')
        for url in extract_urls(text):
            print(f" - {url.rstrip(".")}")

    else:
        print("Text could not be loaded successfully")

def main():
    parser = argparse.ArgumentParser(description="Text Analyzer")
    parser.add_argument("filepath", help="Path to the text file")
    args = parser.parse_args()

    text = load_text(args.filepath)
    display_results(text)

if __name__ == "__main__":
    main()
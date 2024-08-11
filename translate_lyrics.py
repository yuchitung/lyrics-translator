import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def translate_text(text, source_lang="ko", target_lang="繁體中文"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Translate the following text from {source_lang} to {target_lang}."},
            {"role": "user", "content": text}
        ]
    )
    print(response)

    return response.choices[0].message.content.strip()

def translate_lyrics(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    translated_text = translate_text(text)
    translated_file_path = file_path.replace('.txt', '-translated.txt')

    with open(translated_file_path, 'w', encoding='utf-8') as f:
        f.write(translated_text)

def main():
    lyrics_directory = 'text'
    for filename in os.listdir(lyrics_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(lyrics_directory, filename)
            translate_lyrics(file_path)

if __name__ == "__main__":
    main()


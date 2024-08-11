import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def fetch_lyrics(url, file_index):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title_tag = soup.select_one('header.pgTitle h1')
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = "No Title Found"

    lyrics_tag = soup.find('div', class_='lyricsContainer').find('xmp')
    lyrics = lyrics_tag.text.strip() if lyrics_tag else 'No Lyrics Found'

    directory = 'text'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_name = f'{directory}/{file_index}-lyrics.txt'
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(title + '\n\n')
        f.write(lyrics)

def get_lyrics_urls(list_url):
    response = requests.get(list_url)
    soup = BeautifulSoup(response.content, "html.parser")

    track_links = soup.select('td a.trackInfo')
    urls = [link.get('href') for link in track_links if link.get('href').startswith('https')]
    return urls

def main():
    lyrics_list_url = os.getenv('LYRICS_LIST_URL')
    print(f"LYRICS_LIST_URL: {lyrics_list_url}")
    if not lyrics_list_url:
        print("Error: LYRIC_LIST_URL is not set in the environment variables.")
    else:
        lyrics_urls = get_lyrics_urls(lyrics_list_url)
        for index, url in enumerate(lyrics_urls, start=1):
            print(f"Fetching lyrics from: {url}")
            fetch_lyrics(url, index)

if __name__ == "__main__":
    main()


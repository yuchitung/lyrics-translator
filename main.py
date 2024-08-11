import fetch_lyrics
import translate_lyrics
import google_docs_integration

def main():
    fetch_lyrics.main()
    translate_lyrics.main()
    google_docs_integration.create_google_doc()


if __name__ == "__main__":
    main()

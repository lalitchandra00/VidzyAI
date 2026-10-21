import os
from urllib.parse import quote

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from youtube_transcript_api.proxies import GenericProxyConfig
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()


def create_transcript_api():
    """Create a transcript client using ProxyScrape credentials when configured."""
    host = os.getenv("PROXYSCRAPE_PROXY_HOST")
    port = os.getenv("PROXYSCRAPE_PROXY_PORT")
    username = os.getenv("PROXYSCRAPE_PROXY_USERNAME")
    password = os.getenv("PROXYSCRAPE_PROXY_PASSWORD")

    if not host and not port and not username and not password:
        return YouTubeTranscriptApi()

    if not host or not port:
        raise RuntimeError(
            "Both PROXYSCRAPE_PROXY_HOST and PROXYSCRAPE_PROXY_PORT must be configured."
        )

    credentials = ""
    if username or password:
        if not username or not password:
            raise RuntimeError(
                "Both PROXYSCRAPE_PROXY_USERNAME and "
                "PROXYSCRAPE_PROXY_PASSWORD must be configured together."
            )
        credentials = f"{quote(username, safe='')}:{quote(password, safe='')}@"

    proxy_url = f"http://{credentials}{host}:{port}"
    return YouTubeTranscriptApi(
        proxy_config=GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url,
        )
    )


def get_transcript_chunks(video_id: str):
    """Fetches YouTube transcript and splits it into text chunks."""
    api = create_transcript_api()
    transcript = api.fetch(video_id, languages=["en", "hi", "es", "fr", "de"])
    transcript_list = transcript.to_raw_data()
    transcript_text = " ".join(chunk["text"] for chunk in transcript_list)

    if not transcript_text.strip():
        raise ValueError("Transcript is empty.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.create_documents([transcript_text])

# Standalone terminal testing
if __name__ == "__main__":
    vid = input("Paste the Video ID here: ").strip()
    try:
        chunks = get_transcript_chunks(vid)
        print(f"Success! Generated {len(chunks)} chunks.")
    except TranscriptsDisabled:
        print("No captions available for this video.")
    except Exception as e:
        print(f"Error: {e}")

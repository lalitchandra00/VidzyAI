from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_transcript_chunks(video_id: str):
    """Fetches YouTube transcript and splits it into text chunks."""
    api = YouTubeTranscriptApi()
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

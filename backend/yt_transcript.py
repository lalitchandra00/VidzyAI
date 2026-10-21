from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

from langchain.text_splitter import RecursiveCharacterTextSplitter

video_id = input("Paste the Video ID here: ").strip()

try:
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en", "hi", "es", "fr", "de"])
    transcript_list = transcript.to_raw_data()
    transcript_text = " ".join(chunk["text"] for chunk in transcript_list)
    print(transcript_text[:500], "...")

except TranscriptsDisabled:
    print("No captions available for this video.")
except Exception as e:
    print(f"Error: {e}")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([transcript_text])
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import modular components from your project files
from yt_transcript import get_transcript_chunks
from database import create_retriever
from chain import get_rag_chain

app = FastAPI(title="Vidzy AI Backend", version="1.0.0")

# Enable CORS for Microsoft Edge / Chrome extensions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for active RAG chains per video_id
chains_cache = {}

class ProcessVideoRequest(BaseModel):
    video_id: str
    force: bool = False

class ChatRequest(BaseModel):
    video_id: str
    question: str

def initialize_chain_for_video(video_id: str):
    """Fetches transcript, indexes into vector DB, and caches the RAG chain."""
    try:
        chunks = get_transcript_chunks(video_id)
        retriever = create_retriever(chunks)
        chain = get_rag_chain(retriever)
        chains_cache[video_id] = chain
        return len(chunks)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def home():
    return {"status": "running", "message": "Vidzy AI Backend is live!"}

@app.post("/api/process-video")
def process_video(req: ProcessVideoRequest):
    video_id = req.video_id.strip()
    if not video_id:
        raise HTTPException(status_code=400, detail="video_id cannot be empty")

    if not req.force and video_id in chains_cache:
        return {"status": "cached", "video_id": video_id, "message": "Video already indexed"}

    chunks_count = initialize_chain_for_video(video_id)
    return {
        "status": "success",
        "video_id": video_id,
        "chunks_indexed": chunks_count,
        "message": "Video indexed successfully"
    }

@app.post("/api/chat")
def chat(req: ChatRequest):
    video_id = req.video_id.strip()
    question = req.question.strip()

    if not video_id or not question:
        raise HTTPException(status_code=400, detail="Both video_id and question are required")

    # If this video hasn't been indexed yet, index it now
    if video_id not in chains_cache:
        initialize_chain_for_video(video_id)

    chain = chains_cache[video_id]
    try:
        answer = chain.invoke(question)
        return {"video_id": video_id, "question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

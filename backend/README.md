# Backend Folder

This folder contains everything that powers VidzyAI behind the scenes. It takes YouTube video transcripts, processes them, and answers questions using AI. 

## Files and How They Work

### `main.py`
This is the main entry point for the backend. It runs a web server that the browser extension talks to. 

- Creates the web server and allows the extension to connect to it.
- Has two main functions: one to process/index a video (get its transcript ready), and one to chat (answer questions about a video).
- Keeps track of videos that have already been processed so it doesn't have to do the work again.

### `yt_transcript.py`
This file gets the transcript from YouTube videos. 

- Connects to YouTube to download the subtitles/transcript for a video.
- Can use a proxy if needed (for getting around any access issues).
- Breaks the transcript into smaller chunks so the AI can search through it more easily.
- Can be tested directly from the terminal to see if a video's transcript can be fetched.

### `embeddings.py`
This file sets up how the text gets converted into a format the AI can understand for searching. 

- Uses Google's AI to turn text chunks into numerical representations (embeddings).
- These help the system find the parts of a transcript that are most relevant to your question.

### `database.py`
This file creates a searchable library of the video's transcript. 

- Takes all the transcript chunks and stores them in a FAISS database (a special search index).
- Creates a "retriever" that can quickly find the most relevant parts of the transcript when you ask a question.

### `prompt.py`
This file tells the AI how to behave when answering questions. 

- Gives the AI strict instructions: only answer from the video's transcript, don't make things up.
- If the answer isn't in the transcript, it will say it doesn't know.

### `chat_model.py`
This file sets up which AI model is used to answer questions. 

- Connects to Google's Gemini AI model.
- Configures how creative or precise the answers should be (keeps them focused and accurate).

### `chain.py`
This file puts everything together for answering questions. 

- Combines the search results from the transcript with your question.
- Sends them to the AI with the instructions from the prompt.
- Returns the clean answer back to the user.

### `requirements.txt`
Lists all the Python packages needed to run the backend.

### `.env`
Stores secret keys and settings like the Google API key and proxy details. This file should never be shared publicly.

### `SourceCode.ipynb`
A notebook file used during development to test and build the project.

## How It All Works Together

1. When you ask to process a video, `main.py` calls `yt_transcript.py` to get the transcript.
2. `embeddings.py` converts those chunks into searchable form.
3. `database.py` stores them in a search index.
4. `chain.py` links the search, prompt, and AI model together.
5. When you ask a question, it finds relevant parts of the transcript and `chat_model.py` gives you an answer based on them.

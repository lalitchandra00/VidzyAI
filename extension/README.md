# Extension Folder

This folder contains the browser extension that you use with VidzyAI. It adds a small popup to your Chrome or Microsoft Edge browser so you can chat with YouTube videos directly. 

## Files and How They Work

### `manifest.json`
This is the configuration file for the browser extension. 

- Tells the browser what the extension is called and what it does.
- Lists what permissions it needs (access to YouTube tabs, storage, etc.).
- Points to the popup window and icons.
- Says it can connect to the VidzyAI backend.

### `popup.html`
This is the layout/design of the extension popup window. 

- Shows the extension header with the VidzyAI logo.
- Has different screens: one for when you're not on a YouTube video, and one for when you are.
- Shows the video ID it's working with.
- Has a chat area where messages appear.
- Includes quick buttons for common questions like "Summarize this video".
- Has a text box to type your own questions.

### `popup.css`
This styles how the popup looks. 

- Makes it look clean and modern.
- Styles the chat bubbles, buttons, and different states.
- Handles the loading spinner and status badges.

### `popup.js`
This is the brain of the extension. It makes everything interactive. 

- **Detects YouTube videos** - Checks if you're on a YouTube watch page, shorts, or embed and grabs the video ID.
- **Talks to the backend** - Sends the video to be processed and sends your questions to get answers.
- **Manages the chat** - Shows your messages and the AI's responses in the chat window.
- **Saves your history** - Remembers your past conversations for each video using the browser's storage.
- **Shows status** - Tells you if it's connecting, indexing the video, ready to chat, or if there's an error.
- **Handles quick prompts** - Lets you click the suggestion buttons to ask common questions instantly.

### `icons/` folder
Contains the extension icons in different sizes (16x16, 48x48, 128x128) that show up in your browser.

## How It Works

1. You click the VidzyAI extension icon while watching a YouTube video.
2. The extension figures out which video you're watching and tells the backend to prepare it.
3. While it's preparing, you'll see a loading message.
4. Once ready, you can type questions or click quick prompts.
5. Your question goes to the backend, gets answered using the video transcript, and comes back to show in the chat.
6. Everything is saved so you can come back later and continue the conversation.

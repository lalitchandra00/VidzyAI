# Installation Guide

Since the backend is already deployed, you don't need to set up anything locally. Just install the extension and start using it. 

## What You'll Need

- Google Chrome or Microsoft Edge browser
- Internet connection

## Step 1: Install the Extension

We have a ready-to-use extension zip file in this folder. 

1. Go to the `installation` folder in the VidzyAI project
2. Find `vidzyai-edge-extension.zip`
3. Extract/unzip that file to a new folder on your computer (keep it somewhere safe)

## Step 2: Add to Your Browser (Developer Mode)

Since this is for testing before paid publishing, we'll load it in developer mode.

### For Microsoft Edge

1. Open Microsoft Edge and go to `edge://extensions/`
2. Turn on "Developer mode" (toggle in the bottom left or top right)
3. Click "Load unpacked"
4. Select the extracted folder from Step 1
5. The VidzyAI extension should now appear in your extensions list

### For Google Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Turn on "Developer mode" (toggle in the top right)
3. Click "Load unpacked"
4. Select the extracted folder from Step 1
5. The VidzyAI extension should now appear in your extensions list

## Step 3: Start Using VidzyAI

1. Open any YouTube video in your browser
2. Click the VidzyAI extension icon in your browser toolbar
3. The extension will automatically detect the video and start preparing it
4. Once it's ready, just type your question or click one of the quick buttons like "Summary"
5. Start chatting with the video!

## Tips & Troubleshooting

- **Video won't load**: Some videos don't have transcripts (no captions). VidzyAI needs transcripts to work, so try a different video with captions/subtitles.
- **Parser/API issues**: Parser problems may occur because of usage of the YouTube transcript API. If this happens, try again later or try a different video.
- **First time is slower**: The first time you ask about a video, it needs to download and process the transcript. After that, it will be faster.
- **Close and reopen**: If something seems stuck, close the extension popup and click it again.
- **Keep developer mode on**: As long as you're using it in developer mode for testing, just keep it loaded like this.

const BACKEND_URL = "http://127.0.0.1:8000";

let currentVideoId = null;
let isIndexing = false;

// DOM Elements
const viewNotYoutube = document.getElementById("view-not-youtube");
const viewActiveVideo = document.getElementById("view-active-video");
const videoIdDisplay = document.getElementById("video-id-display");
const statusBadge = document.getElementById("status-badge");
const indexingBanner = document.getElementById("indexing-banner");
const indexingText = document.getElementById("indexing-text");
const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const reindexBtn = document.getElementById("reindex-btn");
const quickPrompts = document.getElementById("quick-prompts");

// Initialize on popup load
document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  await detectActiveVideo();
});

function setupEventListeners() {
  sendBtn.addEventListener("click", handleSendMessage);

  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  reindexBtn.addEventListener("click", () => {
    if (currentVideoId && !isIndexing) {
      processVideo(currentVideoId, true);
    }
  });

  quickPrompts.addEventListener("click", (e) => {
    const pill = e.target.closest(".pill");
    if (pill && !sendBtn.disabled) {
      userInput.value = pill.dataset.prompt;
      handleSendMessage();
    }
  });
}

// 1. Detect current browser tab URL and extract video ID
async function detectActiveVideo() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.url) {
      showNotYouTubeView();
      return;
    }

    const videoId = extractYouTubeVideoId(tab.url);
    if (!videoId) {
      showNotYouTubeView();
      return;
    }

    currentVideoId = videoId;
    showActiveVideoView(videoId);
    await loadStoredChat(videoId);
    await processVideo(videoId);
  } catch (err) {
    console.error("Error detecting tab:", err);
    showNotYouTubeView();
  }
}

function extractYouTubeVideoId(url) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes("youtube.com")) {
      if (parsed.pathname === "/watch") {
        return parsed.searchParams.get("v");
      }
      if (parsed.pathname.startsWith("/shorts/")) {
        return parsed.pathname.split("/")[2];
      }
      if (parsed.pathname.startsWith("/embed/")) {
        return parsed.pathname.split("/")[2];
      }
    } else if (parsed.hostname === "youtu.be") {
      return parsed.pathname.slice(1);
    }
  } catch (e) {
    return null;
  }
  return null;
}

function showNotYouTubeView() {
  viewNotYoutube.classList.remove("hidden");
  viewActiveVideo.classList.add("hidden");
  updateBadge("No Video", "badge-waiting");
}

function showActiveVideoView(videoId) {
  viewNotYoutube.classList.add("hidden");
  viewActiveVideo.classList.remove("hidden");
  videoIdDisplay.textContent = videoId;
}

function updateBadge(text, className) {
  statusBadge.className = `badge ${className}`;
  statusBadge.textContent = text;
}

// 2. Call Backend API to Index the Video
async function processVideo(videoId, force = false) {
  isIndexing = true;
  indexingBanner.classList.remove("hidden");
  indexingBanner.className = "banner banner-loading";
  indexingText.textContent = "Fetching transcript & building embeddings...";
  updateBadge("Indexing...", "badge-waiting");
  sendBtn.disabled = true;

  try {
    const response = await fetch(`${BACKEND_URL}/api/process-video`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: videoId, force: force })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server returned ${response.status}`);
    }

    const data = await response.json();
    indexingBanner.classList.add("hidden");
    updateBadge("Ready", "badge-ready");
    sendBtn.disabled = false;
  } catch (err) {
    console.error("Indexing failed:", err);
    indexingBanner.className = "banner banner-error";
    indexingText.textContent = err.message.includes("Failed to fetch")
      ? "Backend not reachable (run backend server on :8000)"
      : `Error: ${err.message}`;
    updateBadge("Offline", "badge-error");
    sendBtn.disabled = false; // allow typing in case user starts server
  } finally {
    isIndexing = false;
  }
}

// 3. Send Question to RAG Backend
async function handleSendMessage() {
  const query = userInput.value.trim();
  if (!query || !currentVideoId) return;

  userInput.value = "";
  appendMessage(query, "user");

  const thinkingId = appendMessage("Thinking...", "bot", true);
  sendBtn.disabled = true;

  try {
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_id: currentVideoId,
        question: query
      })
    });

    if (!response.ok) {
      const errJson = await response.json().catch(() => ({}));
      throw new Error(errJson.detail || `Backend error: ${response.status}`);
    }

    const result = await response.json();
    updateMessage(thinkingId, result.answer || "No response received.");
    saveChatHistory(currentVideoId);
  } catch (err) {
    updateMessage(
      thinkingId,
      `⚠️ Error: ${err.message}. Make sure your backend server is running on http://127.0.0.1:8000`
    );
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

// UI Helpers
function appendMessage(text, sender, isTemporary = false) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `message message-${sender}`;
  const id = "msg-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4);
  msgDiv.id = id;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  msgDiv.appendChild(bubble);
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return id;
}

function updateMessage(id, newText) {
  const msgDiv = document.getElementById(id);
  if (msgDiv) {
    const bubble = msgDiv.querySelector(".bubble");
    if (bubble) bubble.textContent = newText;
  }
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Persistence with chrome.storage.local
async function loadStoredChat(videoId) {
  return new Promise((resolve) => {
    chrome.storage.local.get([`chat_${videoId}`], (result) => {
      const history = result[`chat_${videoId}`];
      if (history && history.length > 0) {
        chatMessages.innerHTML = "";
        history.forEach((m) => appendMessage(m.text, m.sender));
      }
      resolve();
    });
  });
}

function saveChatHistory(videoId) {
  const messages = [];
  const messageElements = chatMessages.querySelectorAll(".message");
  messageElements.forEach((el) => {
    const sender = el.classList.contains("message-user") ? "user" : "bot";
    const text = el.querySelector(".bubble")?.textContent || "";
    messages.push({ sender, text });
  });

  chrome.storage.local.set({ [`chat_${videoId}`]: messages });
}


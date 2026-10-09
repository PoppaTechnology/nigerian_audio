# Nigerian Audio Scraper & REST API

A Django REST Framework backend designed to extract, convert, and manage Nigerian language audio clips from online media URLs (YouTube, Vimeo, and other supported platforms). The application converts media to MP3 format, organizes audio files by language category, and provides a REST API for frontend web and mobile applications.

---

## 📌 Features

- **Multi-Platform Audio Extraction**: Extracts audio streams from online video and audio URLs supported by `yt-dlp`.
- **Automated MP3 Conversion**: Converts downloaded streams to MP3 format using FFmpeg with unique identifiers to prevent collisions.
- **Categorized Storage**: Organizes audio files by Nigerian language categories.
- **Clean RESTful API**: Endpoints to scrape/download, list/filter, retrieve details, and delete audio records.
- **Automatic Storage Cleanup**: Automatically removes physical audio files when their corresponding database records are deleted.

---

## 🗣️ Supported Language Categories

- `Hausa`
- `Igbo`
- `Yoruba`
- `Efik`
- `Tiv`

---

## 🛠️ Requirements & Setup

### Prerequisites

- **Python 3.10+**
- **FFmpeg** (installed and available in system `PATH`)

### Quickstart

1. **Clone the repository and navigate into the folder**:
   ```bash
   git clone <repository-url>
   cd nigerian_audio
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the API server**:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/`.

---

## 📡 API Endpoints Reference

Base URL: `http://localhost:8000` (or your deployed server domain)

| Method | Endpoint | Description | Request Body / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/` | Scrapes audio from an online URL, converts to MP3, and saves it | `{ "content_link": string, "category": string }` |
| `GET` | `/audios/` | Lists all audio records | Optional query param: `?category=<category_name>` |
| `GET` | `/audios/<id>/` | Retrieves single audio record by ID | URL path parameter `id` (integer) |
| `DELETE` | `/audios_delete/<id>/` | Deletes an audio record and its physical file | URL path parameter `id` (integer) |

---

### Endpoint Details

#### 1. `POST /` — Scrape & Convert Audio

Extracts audio from a supported media URL and creates a new entry.

- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "content_link": "https://www.youtube.com/watch?v=EXAMPLE_ID",
    "category": "Yoruba"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "id": 1,
    "title": "Audio Title Example",
    "content_link": "https://www.youtube.com/watch?v=EXAMPLE_ID",
    "audio_file": "/media/audios/Yoruba/Audio_Title_Example_a1b2c3d4.mp3",
    "category": "Yoruba",
    "timestamp": "2026-10-09T12:00:00Z"
  }
  ```

#### 2. `GET /audios/` — List Audios

Retrieves all audio entries, or filters them by category.

- **Query Parameters**:
  - `category` *(optional)*: e.g., `/audios/?category=Hausa`
- **Response (`200 OK`)**:
  ```json
  [
    {
      "id": 1,
      "title": "Hausa News Episode 1",
      "content_link": "https://www.example.com/video",
      "audio_file": "/media/audios/Hausa/Hausa_News_Episode_1_1234abcd.mp3",
      "category": "Hausa",
      "timestamp": "2026-10-09T12:00:00Z"
    }
  ]
  ```

#### 3. `GET /audios/<id>/` — Retrieve Audio

Fetches metadata and playback URL for a specific audio item.

- **Response (`200 OK`)**:
  ```json
  {
    "id": 1,
    "title": "Hausa News Episode 1",
    "content_link": "https://www.example.com/video",
    "audio_file": "/media/audios/Hausa/Hausa_News_Episode_1_1234abcd.mp3",
    "category": "Hausa",
    "timestamp": "2026-10-09T12:00:00Z"
  }
  ```

#### 4. `DELETE /audios_delete/<id>/` — Delete Audio

Deletes the audio metadata and associated MP3 file from storage.

- **Response (`200 OK`)**:
  ```json
  {
    "message": "Audio  deleted successfully"
  }
  ```

---

## 💻 Frontend Integration Guide

Here is how frontend client applications (React, Vue, Next.js, or Vanilla JS) can interact with this API.

### 1. API Client Helper (JavaScript / TypeScript)

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Replace with your production API URL

export const audioApi = {
  // Scrape and download a new audio
  scrapeAudio: async (contentLink, category) => {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content_link: contentLink, category }),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Failed to scrape audio');
    }
    return response.json();
  },

  // Fetch audio list (with optional category filter)
  getAudios: async (category = '') => {
    const url = category
      ? `${API_BASE_URL}/audios/?category=${encodeURIComponent(category)}`
      : `${API_BASE_URL}/audios/`;
    const response = await fetch(url);
    if (!response.ok) {
      if (response.status === 404) return []; // No audios found
      throw new Error('Failed to fetch audios');
    }
    return response.json();
  },

  // Get a single audio item
  getAudioById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/audios/${id}/`);
    if (!response.ok) throw new Error('Audio not found');
    return response.json();
  },

  // Delete an audio item
  deleteAudio: async (id) => {
    const response = await fetch(`${API_BASE_URL}/audios_delete/${id}/`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete audio');
    return response.json();
  },

  // Helper to build full media stream URL for HTML5 <audio> players
  getMediaUrl: (audioFilePath) => {
    if (!audioFilePath) return '';
    return audioFilePath.startsWith('http')
      ? audioFilePath
      : `${API_BASE_URL}${audioFilePath}`;
  },
};
```

---

### 2. Frontend Usage Example (React Component)

```jsx
import React, { useState, useEffect } from 'react';
import { audioApi } from './api';

const CATEGORIES = ['Hausa', 'Igbo', 'Yoruba', 'Efik', 'Tiv'];

export default function AudioDashboard() {
  const [audios, setAudios] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [urlInput, setUrlInput] = useState('');
  const [categoryInput, setCategoryInput] = useState('Yoruba');
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  // Load audios on mount or when category filter changes
  useEffect(() => {
    loadAudios();
  }, [selectedCategory]);

  const loadAudios = async () => {
    try {
      const data = await audioApi.getAudios(selectedCategory);
      setAudios(data);
    } catch (err) {
      console.error(err);
    }
  };

  // Handle Scraping / Submitting New URL
  const handleScrape = async (e) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    setLoading(true);
    setStatusMessage('Downloading and converting audio... Please wait.');
    try {
      await audioApi.scrapeAudio(urlInput, categoryInput);
      setUrlInput('');
      setStatusMessage('Audio successfully saved!');
      loadAudios(); // Refresh list
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Handle Deleting Audio
  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this audio?')) return;
    try {
      await audioApi.deleteAudio(id);
      setAudios((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Nigerian Audio Hub</h1>

      {/* Scraper Form */}
      <form onSubmit={handleScrape} style={{ marginBottom: '24px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <input
          type="url"
          placeholder="Paste video/media URL..."
          value={urlInput}
          onChange={(e) => setUrlInput(e.target.value)}
          required
          style={{ flex: '1', minWidth: '240px', padding: '8px' }}
        />
        <select
          value={categoryInput}
          onChange={(e) => setCategoryInput(e.target.value)}
          style={{ padding: '8px' }}
        >
          {CATEGORIES.map((cat) => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        <button type="submit" disabled={loading} style={{ padding: '8px 16px' }}>
          {loading ? 'Processing...' : 'Extract & Save'}
        </button>
      </form>

      {statusMessage && <p style={{ fontWeight: 'bold' }}>{statusMessage}</p>}

      {/* Filter Tabs */}
      <div style={{ marginBottom: '16px', display: 'flex', gap: '8px' }}>
        <button
          onClick={() => setSelectedCategory('')}
          style={{ fontWeight: selectedCategory === '' ? 'bold' : 'normal' }}
        >
          All
        </button>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{ fontWeight: selectedCategory === cat ? 'bold' : 'normal' }}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Audio List & Playback */}
      <div>
        {audios.length === 0 ? (
          <p>No audio files found.</p>
        ) : (
          audios.map((audio) => (
            <div
              key={audio.id}
              style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '12px',
              }}
            >
              <h3>{audio.title}</h3>
              <p style={{ fontSize: '13px', color: '#666' }}>
                Category: <strong>{audio.category}</strong> | Added: {new Date(audio.timestamp).toLocaleDateString()}
              </p>

              {/* Native HTML5 Audio Player */}
              <audio
                controls
                src={audioApi.getMediaUrl(audio.audio_file)}
                style={{ width: '100%', margin: '8px 0' }}
              />

              <div>
                <button
                  onClick={() => handleDelete(audio.id)}
                  style={{ color: 'red', cursor: 'pointer' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
```

---

### 3. Key Frontend Considerations

- **CORS Configuration**: If the frontend is hosted on a separate domain/port (e.g. `localhost:3000` or `localhost:5173`), ensure `django-cors-headers` is installed and configured in `INSTALLED_APPS` and `MIDDLEWARE` in Django settings.
- **Audio Streaming**: The `audio_file` field returns a relative media path (e.g. `/media/audios/Yoruba/...`). Prefix it with the API base URL to stream in `<audio src="...">` elements or custom audio visualizers.
- **Async Scraping Feedback**: Because downloading and converting audio takes a few seconds depending on the file size, always provide a loading state or spinner in the frontend UI while calling `POST /`.

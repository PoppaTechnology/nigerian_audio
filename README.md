# Nigerian Audio Scraper & REST API

A Django REST Framework backend designed to extract, convert, and manage Nigerian language audio clips from online media URLs (YouTube, and other supported platforms). The application converts media to MP3 format, organizes audio files by language category, and provides a REST API for frontend web and mobile applications.

---

## Features

- **Multi-Platform Audio Extraction**: Extracts audio streams from online video and audio URLs supported by `yt-dlp`.
- **Automated MP3 Conversion**: Converts downloaded streams to MP3 format using FFmpeg with unique identifiers to prevent collisions.
- **Categorized Storage**: Organizes audio files by Nigerian language categories.
- **Clean RESTful API**: Endpoints to scrape/download, list/filter, retrieve details, and delete audio records.
- **Automatic Storage Cleanup**: Automatically removes physical audio files when their corresponding database records are deleted.

---

## Supported Language Categories

- `Hausa`
- `Igbo`
- `Yoruba`
- `Efik`
- `Tiv`

---

## Requirements & Setup

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

## API Endpoints Reference

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
  
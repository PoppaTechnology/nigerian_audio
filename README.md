# Nigerian Audio Scraper & REST API

A Django and Django REST Framework (DRF) application designed to scrape, extract, convert, and manage Nigerian language audio datasets from YouTube. The system downloads audio from provided YouTube URLs, converts them into high-quality MP3 files using FFmpeg, organizes them by language category, and exposes a RESTful API for management and consumption.

---

## 📌 Features

- **YouTube Audio Extraction**: Downloads high-quality audio streams from YouTube videos using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).
- **Automated MP3 Conversion**: Converts audio files to MP3 using [`ffmpeg-python`](https://github.com/kkroening/ffmpeg-python) with sanitized filenames and UUID suffixes to prevent naming collisions.
- **Categorized Storage**: Automatically organizes audio files into category-specific directories (`media/audios/<category>/`).
- **RESTful API**: Endpoints for scraping/downloading, listing with category filters, retrieving audio metadata/streaming URLs, and deleting audio items.
- **Automated Disk Cleanup**: Custom deletion logic that removes the underlying audio file from the filesystem and removes empty category folders.
- **Django Admin**: Built-in administration interface for inspecting and managing audio records.

---

## 🗣️ Supported Language Categories

The system supports categorization under the following Nigerian languages:

- `Hausa`
- `Igbo`
- `Yoruba`
- `Efik`
- `Tiv`

---

## 📁 Project Structure

```text
nigerian_audio/
├── api/                        # REST API application
│   ├── serializers.py          # AudioContent ModelSerializer
│   ├── urls.py                 # API routing definitions
│   └── views.py                # API view functions (scrape, list, get, delete)
├── audio_scraper/              # Core business logic application
│   ├── admin.py                # Admin panel configuration
│   ├── models.py               # AudioContent model & cleanup logic
│   ├── utils.py                # YouTube download & FFmpeg conversion utilities
│   └── migrations/             # Database migration files
├── media/                      # Downloaded and converted audio files (runtime)
│   └── audios/
│       ├── Hausa/
│       ├── Igbo/
│       ├── Yoruba/
│       ├── Efik/
│       └── Tiv/
├── nigerian_audio/             # Django project configuration
│   ├── asgi.py
│   ├── settings.py             # Project settings (INSTALLED_APPS, MEDIA_ROOT, etc.)
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py
├── manage.py                   # Django CLI entrypoint
├── requirements.txt            # Python package dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## 🛠️ Prerequisites

Before getting started, make sure you have the following installed on your machine:

1. **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2. **FFmpeg**: Required on your system `PATH` for audio processing and conversion.
   - **Windows**:
     ```powershell
     winget install "FFmpeg (Essentials Build)"
     # or via Chocolatey
     choco install ffmpeg
     ```
   - **macOS** (via Homebrew):
     ```bash
     brew install ffmpeg
     ```
   - **Ubuntu / Debian**:
     ```bash
     sudo apt update && sudo apt install -y ffmpeg
     ```
   - Verify installation:
     ```bash
     ffmpeg -version
     ```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nigerian_audio
```

### 2. Create and Activate a Virtual Environment

- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional, for Admin Panel)

```bash
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

---

## 📡 API Reference

### 1. Scrape & Download YouTube Audio

Extracts audio from a given YouTube link, converts it to MP3, and creates an `AudioContent` database record.

- **URL**: `/`
- **Method**: `POST`
- **Content-Type**: `application/json`

**Request Body:**
```json
{
  "content_link": "https://www.youtube.com/watch?v=EXAMPLE_ID",
  "category": "Yoruba"
}
```

**Success Response (`200 OK`):**
```json
{
  "id": 1,
  "title": "Example Yoruba Audio Title",
  "content_link": "https://www.youtube.com/watch?v=EXAMPLE_ID",
  "audio_file": "/media/audios/Yoruba/Example_Yoruba_Audio_a1b2c3d4.mp3",
  "category": "Yoruba",
  "timestamp": "2026-10-09T12:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Missing `content_link` or `category`.
- `500 Internal Server Error`: Failed to download or convert YouTube audio.

---

### 2. List Audio Records

Retrieves a list of all audio files. Can optionally filter by category.

- **URL**: `/audios/`
- **Method**: `GET`
- **Query Parameters**:
  - `category` *(optional)*: Filter by language (e.g. `?category=Hausa`)

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/audios/?category=Hausa"
```

**Success Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "title": "Hausa News Broadcast",
    "content_link": "https://www.youtube.com/watch?v=EXAMPLE_ID",
    "audio_file": "/media/audios/Hausa/Hausa_News_Broadcast_e5f6g7h8.mp3",
    "category": "Hausa",
    "timestamp": "2026-10-09T12:00:00Z"
  }
]
```

**Error Response (`404 Not Found`):**
```json
{
  "message": "No audio files found"
}
```

---

### 3. Retrieve Single Audio Record

Fetches detailed metadata and media URL for a specific audio entry.

- **URL**: `/audios/<int:pk>/`
- **Method**: `GET`

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/audios/1/"
```

**Success Response (`200 OK`):**
```json
{
  "id": 1,
  "title": "Hausa News Broadcast",
  "content_link": "https://www.youtube.com/watch?v=EXAMPLE_ID",
  "audio_file": "/media/audios/Hausa/Hausa_News_Broadcast_e5f6g7h8.mp3",
  "category": "Hausa",
  "timestamp": "2026-10-09T12:00:00Z"
}
```

**Error Response (`404 Not Found`):**
```json
{
  "error": "Audio not found"
}
```

---

### 4. Delete Audio Record

Deletes the database entry and removes the corresponding `.mp3` file from disk. If the category directory is empty after deletion, the folder is removed as well.

- **URL**: `/audios_delete/<int:pk>/`
- **Method**: `DELETE`

**Example Request:**
```bash
curl -X DELETE "http://127.0.0.1:8000/audios_delete/1/"
```

**Success Response (`200 OK`):**
```json
{
  "message": "Audio  deleted successfully"
}
```

**Error Response (`404 Not Found`):**
```json
{
  "error": "Audio not found"
}
```

---

## 🛡️ Django Administration

You can access the Django admin panel at:

```text
http://127.0.0.1:8000/admin/
```

Log in using the superuser credentials created in step 5 to view, filter, or delete `AudioContent` records through the UI.

---

## ⚙️ Configuration & Storage Notes

- **Media Root**: Uploaded/converted audio files are stored locally in the `media/` folder defined by `MEDIA_ROOT` in [`nigerian_audio/settings.py`](nigerian_audio/settings.py).
- **Cloud Storage (S3)**: The project includes `django-storages` and `boto3` in `requirements.txt`, making it easy to configure AWS S3 or compatible object storage for production deployments.
- **Production Checklist**:
  - Set `DEBUG = False` in `nigerian_audio/settings.py`.
  - Configure secure `ALLOWED_HOSTS` and a secret key loaded via environment variables.
  - Configure a production-grade database (e.g. PostgreSQL) instead of SQLite.

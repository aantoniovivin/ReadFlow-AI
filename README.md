# ScanDoc AI

ScanDoc AI turns PDF documents into searchable scan pages and structured briefing sections, with term definitions linked back to page locations.

## Run locally

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
python -m pip install --prefer-binary -r requirements.txt
cp .env.example .env  # add GROQ_API_KEY; Openverse credentials are optional
uvicorn main:app --reload --port 8000
```


Openverse image search works anonymously. To use authenticated requests and receive its registered-user rate limits, register an application with the Openverse API and put the returned `client_id` and `client_secret` in `backend/.env` as `OPENVERSE_CLIENT_ID` and `OPENVERSE_CLIENT_SECRET`. Keep the secret private and restart the backend after editing `.env`.

The standard setup uses lightweight local word-analysis rules, so spaCy and its model are not downloaded. To enable the optional spaCy model for richer lemma/POS results, run `python -m pip install --prefer-binary -r requirements-spacy.txt` inside the backend virtual environment. That optional install downloads spaCy and its English model once.

Tesseract OCR must be installed on the host for image-only PDFs (`tesseract-ocr` on Debian/Ubuntu). Clicked words use local analysis (the optional spaCy model provides richer lemma/POS results); Pollinations generates the accompanying diagrams, and Groq generates summaries and contextual meanings. If a provider is unavailable, the backend returns an extract-based summary or a clear message in the word card.

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://localhost:8000`. Uploads are limited by configuration in `backend/main.py`; generated page images are served only for the lifetime of the local process and should be moved to managed storage for deployment.

## API
- `POST /api/documents` multipart PDF upload and processing
- `GET /api/documents/{id}` document metadata, sections and term boxes
- `GET /api/documents/{id}/pages/{n}.png` rendered page image
- `POST /api/documents/{id}/chat` question answering against extracted text
- `DELETE /api/documents/{id}` delete local document data

The app extracts text spans and bounding boxes from digital PDFs. Scanned PDFs use Tesseract TSV boxes when available. Groq output is parsed and validated against Pydantic models; unavailable model output falls back to locally generated sections. The default Groq model is `openai/gpt-oss-120b`.
# ReadFlow-AI

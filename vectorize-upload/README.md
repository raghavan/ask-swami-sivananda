# 📚 Vectorize & Upload to Pinecone

One-time script to process Swami Sivananda's books and upload to Pinecone.

## Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run the upload**:
```bash
python upload_to_pinecone.py
```

## What it does

1. ✅ Loads all PDFs from `../../pdf_books/`
2. ✅ Splits into 1000-character chunks
3. ✅ Creates embeddings using OpenAI (1024 dimensions)
4. ✅ Uploads to Pinecone index: `swami-sivananda-new`
5. ✅ Verifies upload with test query

## Configuration

- **Embedding Model**: `text-embedding-3-small`
- **Dimensions**: 1024
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters

## Time & Cost

- **Time**: ~5-10 minutes for 50 books
- **Cost**: ~$0.50-$2.00 (one-time)

## After Upload

Once complete, you can deploy the chat app (in `../2-chat-app/`) to Vercel!

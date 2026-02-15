# 📚 Vectorize & Upload to Pinecone

One-time script to process Swami Sivananda's books and upload to Pinecone.

## 🔧 One-Time Pinecone Setup

Before running this script, create a free Pinecone index:

1. **Sign up for Pinecone** (Free tier available): https://www.pinecone.io/
2. **Create a new index** with these settings:
   - **Index Name**: `swami-sivananda-new` (or your preferred name)
   - **Dimensions**: `1024`
   - **Metric**: `cosine`
   - **Cloud Provider**: AWS (recommended)
   - **Region**: us-east-1 (recommended)
3. **Get your API key** from the Pinecone dashboard
4. Note your index name for the `.env` configuration below

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

Once complete, you can deploy the chat app (in `../chat-app/`) to Vercel!

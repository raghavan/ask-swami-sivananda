# 🕉️ Ask Swami Sivananda - Complete Solution

Chat with the wisdom of Swami Sivananda's 300+ books using AI.

## 📦 Projects

### 1️⃣ Vectorize & Upload (`1-vectorize-upload/`)

One-time script to process PDFs and upload to Pinecone.

**Run locally once:**
```bash
cd 1-vectorize-upload
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python upload_to_pinecone.py
```

### 2️⃣ Chat App (`2-chat-app/`)

Production chat interface deployed on Vercel.

**Deploy to Vercel:**
```bash
cd 2-chat-app
vercel
```

## 🔑 Required API Keys

1. **Pinecone** (Free): https://www.pinecone.io/
2. **OpenAI** (Paid): https://platform.openai.com/

## 🎯 Quick Start

### Step 1: Upload Books to Pinecone (One Time)

```bash
cd 1-vectorize-upload
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python upload_to_pinecone.py
```

Time: ~5-10 minutes
Cost: ~$0.50-$2.00 (one-time)

### Step 2: Deploy Chat App to Vercel

```bash
cd ../2-chat-app
npm install -g vercel
vercel login
vercel
```

Add environment variables in Vercel:
- `PINECONE_API_KEY`
- `PINECONE_INDEX_NAME`
- `OPENAI_API_KEY`

Time: ~2 minutes
Cost: FREE (Vercel Hobby plan)

### Step 3: Share! 🎉

Your app is live at: `https://your-app.vercel.app`

## 🏗️ Architecture

```
User Question
    ↓
Frontend (Vercel)
    ↓
API (/api/chat)
    ↓
OpenAI Embedding (1024 dims)
    ↓
Pinecone Vector Search
    ↓
OpenAI Chat Completion
    ↓
Response to User
```

## 💰 Total Costs

| Service | Cost |
|---------|------|
| Vercel | FREE |
| Pinecone | FREE (1GB tier) |
| OpenAI Embeddings | $0.50 one-time |
| OpenAI Chat | ~$0.01/question |
| **Total** | ~$1-5/month |

## 🌟 Features

✅ No login required
✅ Beautiful UI
✅ Fast responses (~2-3 seconds)
✅ Mobile friendly
✅ Source attribution
✅ Chat history
✅ 100% serverless
✅ Scales automatically

## 📝 Configuration

### Pinecone Index Details

- **Index Name**: `swami-sivananda-new`
- **Dimensions**: 1024
- **Metric**: Cosine
- **Cloud**: AWS (us-east-1)

### OpenAI Models

- **Embeddings**: `text-embedding-3-small` (1024 dims)
- **Chat**: `gpt-4o-mini`

## 🚀 Live Demo

Coming soon: https://ask-sivananda.vercel.app

---

Built with ❤️ to spread the timeless wisdom of Swami Sivananda 🙏

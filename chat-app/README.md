# Ask Swami Sivananda - Chat App

Chat interface to query Swami Sivananda's teachings using Pinecone vector search and OpenAI.

## Project Structure

```
2-chat-app/
├── chat_core.py          # Shared logic (embedding, search, completion)
├── api/
│   └── chat.py           # Vercel serverless function (imports chat_core)
├── dev_server.py         # Local dev server (imports chat_core)
├── public/
│   └── index.html        # Frontend UI
├── vercel.json           # Vercel routing config
└── requirements.txt      # Python dependencies
```

## Environment Variables

```
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=swami-sivananda-new
OPENAI_API_KEY=your-openai-api-key
```

## Local Development

```bash
cp .env.example .env     # add your keys to .env
pip install -r requirements.txt
pip install python-dotenv
python dev_server.py
```

Open http://localhost:3000

## Deploy to Vercel

```bash
npm install -g vercel
vercel login
vercel
```

Add environment variables in Vercel Dashboard (Settings > Environment Variables).

Your app will be live at `https://your-app.vercel.app`.

## How it Works

1. User asks a question via the chat UI
2. Question is embedded using OpenAI (`text-embedding-3-large`)
3. Pinecone returns top 5 matching passages from Swami Sivananda's books
4. OpenAI generates a response in Swami Sivananda's voice
5. Answer and source books are displayed in the chat

"""
One-time script to process PDFs and upload to Pinecone
Run this locally once to populate your Pinecone vector database
"""

import os
import glob
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import sys

# Load environment variables
load_dotenv()

# Configuration
BOOKS_DIR = os.getenv("BOOKS_DIR", "../pdf_books")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "swami-sivananda-new")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI embeddings with 1024 dimensions (more efficient!)
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSION = 1024

def main():
    print("🚀 Starting Pinecone Upload Process\n")
    print("=" * 60)

    # Step 1: Initialize Pinecone
    print("\n1️⃣ Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Check if index exists
    existing_indexes = pc.list_indexes().names()
    print(f"   Existing indexes: {existing_indexes}")

    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"\n   ⚠️  Index '{PINECONE_INDEX_NAME}' not found!")
        print(f"   Creating new index with dimension={EMBEDDING_DIMENSION}...")

        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"   ✅ Index '{PINECONE_INDEX_NAME}' created!")
    else:
        print(f"   ✅ Using existing index: {PINECONE_INDEX_NAME}")

    # Get index stats
    index = pc.Index(PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()
    print(f"   Current vectors in index: {stats.total_vector_count}")

    # Step 2: Load PDFs
    print(f"\n2️⃣ Loading PDFs from {BOOKS_DIR}...")
    if len(sys.argv) > 1:
        pdf_files = [sys.argv[1]]
    else:
        pdf_files = glob.glob(os.path.join(BOOKS_DIR, "*.pdf"))


    if not pdf_files:
        print(f"   ❌ No PDF files found in {BOOKS_DIR}")
        print(f"   Please add PDF files to the directory and try again.")
        return

    print(f"   Found {len(pdf_files)} books:")
    for pdf in pdf_files[:5]:  # Show first 5
        print(f"      - {Path(pdf).name}")
    if len(pdf_files) > 5:
        print(f"      ... and {len(pdf_files) - 5} more")

    # Step 3: Process PDFs
    print(f"\n3️⃣ Processing PDFs...")
    all_documents = []

    for i, pdf_path in enumerate(pdf_files, 1):
        try:
            print(f"   [{i}/{len(pdf_files)}] Processing: {Path(pdf_path).name}")

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            # Add metadata
            book_name = Path(pdf_path).stem
            for doc in documents:
                doc.metadata['book'] = book_name
                doc.metadata['source'] = Path(pdf_path).name

            all_documents.extend(documents)

        except Exception as e:
            print(f"      ⚠️  Error: {e}")

    print(f"   ✅ Loaded {len(all_documents)} pages total")

    # Step 4: Split into chunks
    print(f"\n4️⃣ Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )

    chunks = text_splitter.split_documents(all_documents)
    print(f"   ✅ Created {len(chunks)} chunks")

    # Step 5: Create embeddings and upload
    print(f"\n5️⃣ Creating embeddings and uploading to Pinecone...")
    print(f"   Model: {EMBEDDING_MODEL}")
    print(f"   Dimensions: {EMBEDDING_DIMENSION}")
    print(f"   This may take several minutes...")

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIMENSION
    )

    # Upload to Pinecone
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )

    print(f"   ✅ Upload complete!")

    # Step 6: Verify upload
    print(f"\n6️⃣ Verifying upload...")
    stats = index.describe_index_stats()
    print(f"   Total vectors in Pinecone: {stats.total_vector_count}")

    # Test query
    print(f"\n7️⃣ Testing search...")
    test_results = vectorstore.similarity_search(
        "How to meditate?",
        k=3
    )
    print(f"   Test query: 'How to meditate?'")
    print(f"   Found {len(test_results)} results")
    if test_results:
        print(f"   Top result from: {test_results[0].metadata.get('book', 'Unknown')}")

    print("\n" + "=" * 60)
    print("✅ SUCCESS! Vector database ready!")
    print("=" * 60)
    print(f"\nPinecone Index: {PINECONE_INDEX_NAME}")
    print(f"Total Vectors: {stats.total_vector_count}")
    print(f"Dimension: {EMBEDDING_DIMENSION}")
    print("\nYou can now deploy the chat app! 🚀")

if __name__ == "__main__":
    main()

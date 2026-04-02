from sentence_transformers import SentenceTransformer
import chromadb
import os
from rag_test import extract_text_from_pdf, clean_text, chunk_text

# 1. Persistent ChromaDB — survives restarts
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Delete old collection if exists, create fresh
try:
    client.delete_collection("maternal_health")
except:
    pass

collection = client.create_collection("maternal_health")

# 3. Load model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Load ALL PDFs with metadata
pdf_folder = "data/pdfs"
all_chunks = []
all_metadata = []

print("Processing PDFs...")

for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        path = os.path.join(pdf_folder, file)
        print(f"  -> {file}")
        
        raw_text = extract_text_from_pdf(path)
        cleaned = clean_text(raw_text)
        chunks = chunk_text(cleaned)
        
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadata.append({
                "source": file,      # which PDF
                "file_path": path    # full path
            })

print(f"Total chunks: {len(all_chunks)}")

# 5. Embed + store in batches
BATCH_SIZE = 100

print("Embedding and storing...")

for i in range(0, len(all_chunks), BATCH_SIZE):
    batch_docs = all_chunks[i:i + BATCH_SIZE]
    batch_meta = all_metadata[i:i + BATCH_SIZE]
    batch_ids = [str(i + j) for j in range(len(batch_docs))]
    
    embeddings = model.encode(batch_docs).tolist()
    
    collection.add(
        documents=batch_docs,
        embeddings=embeddings,
        metadatas=batch_meta,
        ids=batch_ids
    )
    
    print(f"  Stored {i + len(batch_docs)} / {len(all_chunks)}")

print("Done. ChromaDB saved to ./chroma_db")

# 6. Test query
query = "Is papaya safe during pregnancy?"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print(f"\nQuery: {query}\n")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"Source: {meta['source']}")
    print(f"Chunk: {doc[:200]}")
    print("---")
from pypdf import PdfReader
import os

# -----------------------------
# STEP 1: Extract text from PDF
# -----------------------------
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    
    return text


# ✅ ADD THIS RIGHT HERE
def clean_text(text):
    text = text.replace("-\n", "")     # fix broken words
    text = text.replace("\n", " ")     # remove bad line breaks
    text = " ".join(text.split())      # normalize spacing
    return text


# -----------------------------
# STEP 2: Chunk text (stable)
# -----------------------------
def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()

    if len(words) == 0:
        return []

    chunks = []
    i = 0

    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += max(1, chunk_size - overlap)  # prevents infinite loops

    return chunks


# -----------------------------
# STEP 3: Load all PDFs
# -----------------------------
pdf_folder = "data/pdfs"

if not os.path.exists(pdf_folder):
    print("❌ Folder not found:", pdf_folder)
    exit()

all_texts = []

print("\n📂 Loading PDFs...\n")

for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        path = os.path.join(pdf_folder, file)

        print(f"📄 Processing: {file}")

        text = extract_text_from_pdf(path)

        print(f"   → Extracted length: {len(text)} chars")

        if len(text.strip()) == 0:
            print(f"⚠️ WARNING: No text extracted from {file}")

        all_texts.append(text)


# -----------------------------
# STEP 4: Chunk everything
# -----------------------------
all_chunks = []

print("\n🔪 Chunking...\n")

for idx, text in enumerate(all_texts):
    chunks = chunk_text(text)

    print(f"Text {idx+1}: {len(chunks)} chunks")

    all_chunks.extend(chunks)


# -----------------------------
# STEP 5: Output check
# -----------------------------
print("\n==============================")
print(f"✅ Total chunks created: {len(all_chunks)}")
print("==============================\n")

if len(all_chunks) > 0:
    print("🔍 Sample chunk:\n")
    print(all_chunks[0][:500])
else:
    print("❌ No chunks created. Something is wrong.")
    query = "What is recommended diet during pregnancy?"

print("\n🔎 Searching manually...\n")

for chunk in all_chunks[:20]:
    if "pregnancy" in chunk.lower():
        print("----")
        print(chunk[:300])
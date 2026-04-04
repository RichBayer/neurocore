from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb
import os


# ----------------------------
# CONFIG
# ----------------------------

KNOWLEDGE_PATH = "/mnt/g/ai/memory/knowledge"
CHROMA_PATH = "/mnt/g/ai/memory/chroma"
COLLECTION_NAME = "jarvis_knowledge"


# ----------------------------
# EMBEDDING MODEL
# ----------------------------

Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ----------------------------
# LOAD + TAG DOCUMENTS
# ----------------------------

documents = SimpleDirectoryReader(
    KNOWLEDGE_PATH,
    recursive=True
).load_data()

print(f"Loaded {len(documents)} documents.")


# 🔥 ADD METADATA BASED ON FILE PATH
for doc in documents:
    file_path = doc.metadata.get("file_path", "")

    # Example:
    # /mnt/g/ai/memory/knowledge/linux/filesystems/df.txt

    parts = file_path.split("/")

    try:
        command = os.path.splitext(parts[-1])[0]
        category = parts[-2]

        doc.metadata["command"] = command
        doc.metadata["category"] = category

    except Exception:
        doc.metadata["command"] = "unknown"
        doc.metadata["category"] = "unknown"


# ----------------------------
# CHROMA SETUP
# ----------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)


# ----------------------------
# BUILD INDEX
# ----------------------------

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

print("Knowledge indexed successfully with metadata.")
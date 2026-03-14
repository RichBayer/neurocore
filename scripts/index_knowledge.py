from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb

# Use the same embedding model everywhere in Jarvis
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load documents from the knowledge directory
documents = SimpleDirectoryReader("/mnt/g/ai/memory/knowledge").load_data()

# Start the persistent Chroma client
chroma_client = chromadb.PersistentClient(
    path="/mnt/g/ai/memory/chroma"
)

# Create or get the Jarvis knowledge collection
collection = chroma_client.get_or_create_collection(
    name="jarvis_knowledge"
)

# Connect LlamaIndex to Chroma
vector_store = ChromaVectorStore(
    chroma_collection=collection
)

# Storage context for the vector store
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# Build the index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

print("Knowledge indexed successfully.")
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb
import sys

# Use the same embedding model used during indexing
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# connect to persistent chroma database
chroma_client = chromadb.PersistentClient(
    path="/mnt/g/ai/memory/chroma"
)

# load the jarvis knowledge collection
collection = chroma_client.get_collection("jarvis_knowledge")

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

# rebuild index interface
index = VectorStoreIndex.from_vector_store(vector_store)

# create retriever
retriever = index.as_retriever(similarity_top_k=2)

# user question
question = " ".join(sys.argv[1:])

if not question:
    print("Please provide a question.")
    sys.exit()

# retrieve context
results = retriever.retrieve(question)

print("\n--- Retrieved Knowledge Context ---\n")

for r in results:
    print(r.text)
    print("\n---\n")
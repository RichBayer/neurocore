#!/usr/bin/env python3

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb
import re


class KnowledgeBase:
    def __init__(self):
        self.retriever = None
        self.initialized = False
        self.collection = None

    def initialize(self):
        if self.initialized:
            return

        print("[Knowledge] Initializing embedding model and vector store...")

        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        Settings.embed_model = embed_model

        chroma_client = chromadb.PersistentClient(
            path="/mnt/g/ai/memory/chroma"
        )

        self.collection = chroma_client.get_or_create_collection(
            name="jarvis_knowledge"
        )

        vector_store = ChromaVectorStore(
            chroma_collection=self.collection
        )

        index = VectorStoreIndex.from_vector_store(vector_store)

        self.retriever = index.as_retriever(similarity_top_k=6)

        self.initialized = True

        print("[Knowledge] Initialization complete.")

    # 🔥 SIMPLE COMMAND DETECTION
    def extract_command(self, question: str):
        match = re.search(r"\b([a-z]+)\b", question.lower())
        if match:
            return match.group(1)
        return None

    def retrieve(self, question: str) -> str:
        if not self.initialized:
            self.initialize()

        command = self.extract_command(question)

        # 🔥 METADATA FILTERED SEARCH
        if command:
            results = self.collection.query(
                query_texts=[question],
                n_results=5,
                where={"command": command}
            )

            docs = results.get("documents", [[]])[0]

            if docs:
                return "\n\n".join(docs)

        # fallback (no match or no results)
        results = self.retriever.retrieve(question)
        context = "\n\n".join(r.text for r in results)

        return context
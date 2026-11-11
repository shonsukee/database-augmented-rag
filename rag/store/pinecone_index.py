"""Chunk, embed and store specification documents in a Pinecone index."""
import logging
import os
from typing import List

from llama_index.core import Document, Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from rag.config import CHUNK_OVERLAP, CHUNK_SIZE, EMBED_BATCH_SIZE, EMBEDDING_MODEL


class PineconeIndex:
    def __init__(self, service: str) -> None:
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY is not set")
        self.client = Pinecone(api_key=api_key)
        # One namespace per service keeps SwitchBot and Fitbit apart inside an index.
        self.service = service

    def store(self, documents: List[Document], index_name: str) -> None:
        Settings.chunk_size = CHUNK_SIZE
        Settings.chunk_overlap = CHUNK_OVERLAP
        Settings.embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL, embed_batch_size=EMBED_BATCH_SIZE)

        vector_store = PineconeVectorStore(
            pinecone_index=self.client.Index(index_name),
            namespace=self.service,
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context)
        logging.info("stored %d documents in index '%s' (namespace '%s')", len(documents), index_name, self.service)

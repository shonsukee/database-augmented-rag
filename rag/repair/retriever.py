"""Semantic search over one specification database (a Pinecone index)."""
import os
from typing import List

from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from rag.config import EMBED_BATCH_SIZE, EMBEDDING_MODEL, SIMILARITY_CUTOFF, SIMILARITY_TOP_K
from rag.repair.prompt import index_name


def retrieve(service: str, database: str, query: str) -> List[NodeWithScore]:
    """Return up to SIMILARITY_TOP_K chunks of `database` that are closest to `query`.

    The specifications of each service live in their own namespace of the index,
    so fewer chunks come back when the namespace holds fewer than the top-k.
    """
    api_key = os.environ.get("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY is not set")

    Settings.embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL, embed_batch_size=EMBED_BATCH_SIZE)
    vector_store = PineconeVectorStore(
        pinecone_index=Pinecone(api_key=api_key).Index(index_name(database)),
        add_sparse_vector=True,
        namespace=service,
    )
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    retriever = VectorIndexRetriever(index=index, similarity_top_k=SIMILARITY_TOP_K)

    nodes = retriever.retrieve(query)
    return SimilarityPostprocessor(similarity_cutoff=SIMILARITY_CUTOFF).postprocess_nodes(nodes)

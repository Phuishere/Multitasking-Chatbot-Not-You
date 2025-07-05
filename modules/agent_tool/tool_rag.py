### IMPORT
import chromadb
from chromadb import Collection
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import streamlit as st
from ..ux_utils import Locale, TextResources, Translator

embed_model: HuggingFaceEmbedding = None
collection: Collection = None

def document_embedding():
    global embed_model
    global collection

    if embed_model is None:
        embed_model_name = "BAAI/bge-small-en-v1.5"
        embed_model = HuggingFaceEmbedding(model_name = embed_model_name)

    # Load document: documents at first is a Document class of llama_index
    documents = SimpleDirectoryReader(input_dir = "./res/documents_rag").load_data()

    # By using get_content() we change it into string type
    documents = [d.get_content() for d in documents]

    # Indexing and storing embedding to disk
    client = chromadb.PersistentClient(path="./chroma")
    try:
        collection = client.get_collection(name="docs")
        if collection.count() > 0:
            print("Using existing collection.")
            return
    except:
        collection = client.create_collection(name="docs")

    for i, d in enumerate(documents): # store each document in a vector embedding database, d should be strings
        embeddings = embed_model.get_text_embedding(d)
        collection.add(
            ids=[str(i)],
            embeddings=embeddings,
            documents=[d]
        )

    # Embed the document (when run for the first time)
    _ = ChromaVectorStore(chroma_collection = collection, persist_dir = "./chroma")

def get_rag_context(message: str, n_results: int = 4,
                    update_database: bool = False, text: TextResources = None):
    # In case text not passed into the function
    if text is None:
        translator = Translator(Locale.ENGLISH)
        text = TextResources(translator = translator)
    
    # Get embed_model and collection
    global embed_model
    global collection
    if (embed_model is None or collection is None) or update_database:
        document_embedding()
        st.success(text.RAG_UPDATE_ANNOUNCEMENT)

    # Clip the max n_results
    if n_results > 5:
        n_results = 5

    # Embed the query
    query_emb = embed_model.get_text_embedding(message)

    # Search for top-k docs
    results = collection.query(
        query_embeddings = [query_emb],
        n_results = n_results,
        include = ["documents"]
    )
    docs = [hit for hit in results["documents"][0]]

    # Prepare prompt with retrieved context
    context = ""
    for i, doc in enumerate(docs):
        context += f"[Chunk {i + 1}]\n"
        context += doc
        if i < (n_results - 1):
            context += "\n\n***\n\n"
    
    return context
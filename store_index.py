from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import os
from src.helper import spit_text, load_pdf_file, download_hugging_face_embeddings


load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_file(data = '../data/')
text_chunks = spit_text(extracted_data)
embeddings = download_hugging_face_embeddings()


# Initialize Pinecone
pc = Pinecone(api_key = PINECONE_API_KEY)
index_name = "medibot-index"

# Check if index exists
if index_name not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name = index_name,
        dimension = 384, 
        metric = "cosine",
        spec = ServerlessSpec(cloud = "aws", region = "us-east-1")
    )


# Embed each chunk and upsert the embeddings into the Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents = text_chunks,
    embedding = embeddings,
    index_name = index_name
)



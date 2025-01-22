from pinecone import Pinecone
from datetime import datetime

pc = Pinecone()
today = datetime.now().strftime("%Y-%m-%d")
index_name = f"heart_disease_articles_{today}"
index_name = index_name.replace('_', '-')
index = pc.Index(index_name)
index.describe_index_stats()

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

from langchain_pinecone import PineconeVectorStore
vector_store = PineconeVectorStore(index=index, embedding=embeddings)


from uuid import uuid4

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = DirectoryLoader('/Users/suliu/Downloads/HealthAssistant/docs/heart_disease_articles_2025-01-20/', glob="*.txt")
documents = loader.load()
# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
document_chunks = text_splitter.split_documents(documents)

uuids = [str(uuid4()) for _ in range(len(document_chunks))]

vector_store.add_documents(documents=document_chunks, ids=uuids)
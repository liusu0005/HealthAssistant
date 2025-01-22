from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone

from .models import db, ChatMessage
from .db_utils import get_user_data


pc = Pinecone()

print("Connecting to Pinecone index")
index_name = 'heart-disease-articles-2025-01-20'
index = pc.Index(index_name)
index.describe_index_stats()

text_field = "text"
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
vectorstore = PineconeVectorStore(index, embeddings, text_field)

print("Creating chains")
template = """You are an experienced doctor specializing in heart diseases. Each day, you encounter patients with various heart conditions and provide them with guidance on how to care for themselves effectively.

Articles:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(streaming=True)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
retriever = vectorstore.as_retriever()

retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

def call_chat(question, user_id):
    user_data = get_user_data(user_id)
    if not user_data:
        raise ValueError("User data not found")

    # Add user data to the prompt context
    user_context = f"Patient Info:\nName: {user_data['name']}, Age: {user_data['age']}, Gender: {user_data['gender']}, Diagnosis: {user_data['diagnosis']}\n\n"
    
    # Append user context to the question
    full_prompt = user_context + question

    answer = ""
    for chunk in retrieval_chain.stream(full_prompt):
        answer += chunk
        yield {"token": chunk}

    chat_message = ChatMessage(user_id=user_id, question=question, answer=answer)
    db.session.add(chat_message)
    db.session.commit()
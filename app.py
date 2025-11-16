from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize embeddings
embeddings = download_hugging_face_embeddings()

# Initialize Pinecone Vector Store
index_name = "medibot-index"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Create retriever
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize Groq LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.4,
    max_tokens=500
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# Create question-answer chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = RetrievalQA.from_chain_type(
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True
)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg
    print(f"User question: {input_text}")
    
    try:
        response = rag_chain.invoke({"input": input_text})
        print(f"Response: {response['answer']}")
        return str(response["answer"])
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"I apologize, but I encountered an error: {str(e)}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

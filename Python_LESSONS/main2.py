import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


# Set Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "LangChain RAG Project.json"

# Load PDF document
loader = PyPDFLoader("Python Programming.pdf")
data = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(data)

# Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Vector store
vector_store = Chroma.from_documents(documents=docs, embedding=embedding_model)

# Retriever
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.5)

# Prompt
system_prompt = (
    """
    You are a helpful AI assistant for Question_Answering.
    To give response of the user's query, you have to use the chunks of retrieved context.
    If you don't know the answer, simply say that you have no idea about that in a graceful manner.
    Give the response in concise and understandable way. Complete your response according to the maximum tokens provided.
    Give the response in Markdown Format.
    If user asks any question which is not in the document or in the retrieved chunks of data then generate response from LLM.
    Always generate the detailed response with examples...Also include the real world scenerios for best understanding.
    \n\n\n
    {context}
    """
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
RAG_Chain = create_retrieval_chain(retriever, question_answer_chain)


def generate_topics_list(pdf_path):
    
    topics = ["Python Basics", "Data Structures", "Functions", "OOP"]
    return topics


def get_content_for_topic(topic):
    response = RAG_Chain.invoke({"input": topic})
    return response["answer"]


def main():
    topics = generate_topics_list("Python Programming.pdf")
    print("Available topics:", topics)

    user_topic = input("Enter a topic: ")
    content = get_content_for_topic(user_topic)
    print(content)

if __name__ == "__main__":
    main()
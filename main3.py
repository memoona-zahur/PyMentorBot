import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Paths
base_path = os.path.dirname(__file__)
pdf_path = os.path.join(base_path, "Python Programming.pdf")
persist_directory = "D:/chroma_db"  # ✅ Change to your D drive or another drive with space

# Load PDF
loader = PyPDFLoader(pdf_path)
data = loader.load()

# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(
    os.path.join(base_path, "LangChain RAG Project.json")
)

# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(data)

# Embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# ✅ Check if vector DB exists already
if not os.path.exists(persist_directory):
    print("Vector store not found. Creating and saving embeddings...")
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    vector_store.persist()
else:
    print("Loading existing vector store...")
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )

# Retriever
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.5)

# Prompt
system_prompt = """
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

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("human", "{input}")]
)

# Chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
RAG_Chain = create_retrieval_chain(retriever, question_answer_chain)

# Sample topic functions
def generate_topics_list():
    return ["Variables & Data Types", "Introducing Lists", "Working with Lists", "if statements",
            "Dictionaries", "User Input & while loop", "Functions", "Classes", "File & Exception"]

def get_content_for_topic(topic):
    response = RAG_Chain.invoke({"input": topic})
    return response["answer"]

def getVariableDataTypes():
    user_topic1 = "What is Variable and Data Types in Python also explain with the help of code but first give code and then text"
    content1 = get_content_for_topic(user_topic1)
    return content1

def Introducing_list():
    user_topic1 = "How to introduce lists in Python also explain with the help of code but first give code and then text"
    content2 = get_content_for_topic(user_topic1)
    return content2

def Working_with_Lists():
    user_topic1 = "Explain the working with lists in Python also explain with the help of code but first give code and then text "
    content3 = get_content_for_topic(user_topic1)
    return content3

def if_statements():
    user_topic1 = "Explain the if_statements in Python also explain with the help of detail multiple if and if else statements code but first give code and then text "
    content = get_content_for_topic(user_topic1)
    return content

def Dictionaries():
    user_topic1 = "Explain the Dictionaries in Python also explain with the help of detail multiple dictionaries code but first give code and then text "
    content = get_content_for_topic(user_topic1)
    return content

def User_Input_and_while_loops():
    user_topic1 = "Explain the user input and while loop in Python also explain with the help of detail code but first give code and then text "
    content = get_content_for_topic(user_topic1)
    return content

def Function1():
    user_topic1 = "Explain the Function in Python also explain with the help of detail multiple function code but first give code and then text "
    content = get_content_for_topic(user_topic1)
    return content

def Classes():
    user_topic1 = "Explain the Classes in Python also explain with the help of detail multiple classes code but first give code and then text "
    content = get_content_for_topic(user_topic1)
    return content

def File_and_Exception():
    user_topic1 = "Explain the File and Exception in Python also explain with the help of detail code but first give code and then text "
    content = get_content_for_topic(user_topic1)
    return content
    

   
# DELETE
def main():
    topic = "Variables & Data Types"
    print(get_content_for_topic(topic))

if __name__ == "__main__":
    main()
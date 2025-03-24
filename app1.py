from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (For development only; restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    api_key="AIzaSyC26Bx9LGbiYFA5l9aj50lvPpJ59G0KWUg"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Python programming assistant. When a user asks a question, provide a detailed response related to Python programming, correcting any spelling mistakes in the user's query. Your responses should be comprehensive, spanning 4 to 5 paragraphs, even if the query seems straightforward. If the user inquires about a topic unrelated to Python, politely inform them of the limitation"),
    ("user", "Question: {question}")
])

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Define request model
class UserInput(BaseModel):
    question: str

@app.post("/get_response")
async def get_response(user_input: UserInput):
    response = chain.invoke({"question": user_input.question})
    return {"response": response}

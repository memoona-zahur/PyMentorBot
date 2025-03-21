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
    allow_origins=["*"],  # Replace "*" with your frontend URL for security
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
    ("system", "You are a helpful Python Programming assistant whenever user ask any question answer the question related in pyhton programming And handle spelling mistakes in user query. Respond in 4 to 5 paragraphs, even if the response is short. If the user asks about a non-Python topic, say sorry."),
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

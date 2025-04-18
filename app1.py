from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from main3 import getVariableDataTypes, Introducing_list, Working_with_Lists, if_statements, Dictionaries, User_Input_and_while_loops, Function1, Classes, File_and_Exception        
import re

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
    ("system", "You are a helpful Python programming assistant. When a user asks a question, provide a response related to Python programming, correcting any spelling mistakes in the user's query. Your responses should be comprehensive. If the user inquires about a topic unrelated to Python, politely inform them of the limitation."),
    ("user", "Question: {question}")
])

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Define request model
class UserInput(BaseModel):
    question: str


def split_response(response_text):
    # This assumes the code is inside triple backticks
    code_match = re.search(r"```(?:python)?(.*?)```", response_text, re.DOTALL)
    code = code_match.group(1).strip() if code_match else ""
    explanation = re.sub(r"```.*?```", "", response_text, flags=re.DOTALL).strip()
    return code, explanation


@app.post("/get_response")
async def get_response(user_input: UserInput):
    # Generate the response
    response = chain.invoke({"question": user_input.question})
    
    # Split the response into code and explanation
    code, explanation = split_response(response)
    
    # Return both code and explanation as the response
    return {"code": code, "explanation": explanation}




@app.get("/getVariableDataTypes")
async def getVariableDataType(): 
    answer2 = getVariableDataTypes()
    code, explanation = split_response(answer2)
    return {"code": code, "explanation": explanation}


@app.get("/Introducing_list")
async def get_list_introduction(): 
    answer2 = Introducing_list()
    code, explanation = split_response(answer2)
    return {"code": code, "explanation": explanation}


@app.get("/Working_with_Lists")
async def get_working_with_lists(): 
    answer3 = Working_with_Lists()
    code, explanation = split_response(answer3)
    return {"code": code, "explanation": explanation}


@app.get("/if_statements")
async def if_Statements(): 
    answer3 = if_statements()
    code, explanation = split_response(answer3)
    return {"code": code, "explanation": explanation}

@app.get("/Dictionaries")
async def Dictionary(): 
    answer = Dictionaries()
    code, explanation = split_response(answer)
    return {"code": code, "explanation": explanation}


@app.get("/User_Input_and_while_loops")
async def User_Input_and_while_loop(): 
    answer = User_Input_and_while_loops()
    code, explanation = split_response(answer)
    return {"code": code, "explanation": explanation}


@app.get("/Function1")
async def Function(): 
    answer = Function1()
    code, explanation = split_response(answer)
    return {"code": code, "explanation": explanation}


@app.get("/Classes")
async def Classe(): 
    answer = Classes()
    code, explanation = split_response(answer)
    return {"code": code, "explanation": explanation}


@app.get("/File_and_Exception")
async def File_and_Exceptions(): 
    answer = File_and_Exception()
    code, explanation = split_response(answer)
    return {"code": code, "explanation": explanation}



from fastapi import Depends, FastAPI
from backend.data_parser import DataParser
import sqlite3  # Asynchronous SQLite library
import logging
from typing import Annotated
from pydantic import BaseModel, StringConstraints
from langchain.chat_models import AzureChatOpenAI
from chains.query_retrieval import Chain
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

llm = AzureChatOpenAI(
    deployment_name="gpt-35-turbo",
    temperature=0,
    verbose=True,
)

chain = Chain(llm)
def get_chain():
    yield chain

def get_llm():
    yield llm
    
class Query(BaseModel):
    # enforce a maximum length of 100 characters on the incoming user query
    query: Annotated[str, StringConstraints(max_length=200)]
    
async def startup_event():
    # Open an asynchronous database connection
    app.state.db = sqlite3.connect("books.sqlite")

    # Initialize the data parser with the database connection
    data_parser = DataParser(app.state.db)

    try:
        data_parser.parse_txt_to_sqlite()
    except Exception as e:
        logging.error(f"Error during data loading: {e}")
    
async def shutdown_event():
    # Close the database connection
    await app.state.db.close()

# Add the event handlers to the application
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/answer")
def answer_query(query: Query, chain: Chain = Depends(get_chain)):
    try:
        response_data = chain.query(query.query)
        return {"response": response_data}
    except Exception as e:
        print(e)
        response = "Sorry, I don't know the answer to that question."
        return {"response": response}
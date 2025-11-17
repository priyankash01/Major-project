import os
from dostenv import load_dotenv # type: ignore
from langchain_openai import OpenAI # type: ignore
from langchain.chains import ConversationChain # type: ignore
from langchain.memory import ConversationBufferMemory # type: ignore

#load .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI-API_KEY not found. please check your .env file")

#Initializing LLM
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)

#store per-user memory sessions
session_memory_map = {}

def get_response(session_id: str, user_query: str) -> str:
    if session_id not in session_memory_map:
        memory = ConversationBufferMemory()
        session_memory_map[session_id] = ConversationChain(llm = llm, memory=memory, verbose= True)

    conversation = session_memory_map[session_id]
    return conversation.predict(input=user_query)

import os
from fastapi import FastAPI # type: ignore
from dotenv import load_dotenv # type: ignore
from models import ChatRequest
from chat_engine import get_response
from crisis import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat

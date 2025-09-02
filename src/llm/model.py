from langchain_anthropic import ChatAnthropic
from src.startup.load_config import *
import os
from pydantic import BaseModel, Field

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set. Please check your .env file or environment variables.")


def get_model():
    llm = ChatAnthropic(
        model="claude-3-7-sonnet-latest",
        temperature=0.05,
        timeout=None,
        max_retries=2,
        max_tokens=20000,
        anthropic_api_key=api_key
    )
    return llm


class SubtopicOutput(BaseModel):
    "Subtopic output"
    subtopic_list: list[str] = Field(description='A list of subtopics')
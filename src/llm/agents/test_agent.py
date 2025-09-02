from langchain_core.messages import SystemMessage
from langgraph.types import Command
from typing import Literal
from src.llm.model import get_model


def test_agent(state) -> Command[Literal['__end__']]:

    model = get_model()

    agent_system_prompt = SystemMessage('You are a helpful AI agent to write a single host transcript for a podcast.')

    # Invoke with custom system prompt
    messages = [
        agent_system_prompt,
        *state['messages']
    ]
    output = model.invoke(messages)

    # Ensure output is a list of messages
    if not isinstance(output, list):
        output = [output]

    return Command(
        goto='__end__',
        update={'messages': output}
    )
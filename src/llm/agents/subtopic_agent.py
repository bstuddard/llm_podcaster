from langchain_core.messages import SystemMessage
from langgraph.types import Command
from typing import Literal
from src.llm.model import get_model, SubtopicOutput
from src.llm.prompts import TOPIC_GENERATING_SYSTEM_PROMPT


def subtopic_agent(state) -> Command[Literal['subtopic_router_agent']]:

    model = get_model()

    # Format the reference document section
    reference_doc = state.get('reference_document', '')
    if reference_doc:
        reference_section = f"Use the following reference document as a guide for content style, examples, and factual information:\n\n{reference_doc}"
    else:
        reference_section = "No reference document provided."

    agent_system_prompt = SystemMessage(TOPIC_GENERATING_SYSTEM_PROMPT.format(
        podcast_topic=state['topic'],
        reference_document_section=reference_section
    ))

    model = model.with_structured_output(SubtopicOutput)

    # Invoke with custom system prompt
    messages = [
        agent_system_prompt,
        *state['messages']
    ]
    output = model.invoke(messages)

    # Update state with the structured output and end
    return Command(
        goto='subtopic_router_agent',
        update={
            'subtopics': output.subtopic_list
        }
    )
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Command
from typing import Literal
from src.llm.model import get_model
from src.llm.prompts import SUBTOPIC_GENERATOR_SYSTEM_PROMPT, SUBTOPIC_SUMMARY_SYSTEM_PROMPT


def subtopic_generator_agent(state) -> Command[Literal['subtopic_router_agent']]:

    # Extract subtopic info from state
    subtopic_input = state.get('current_subtopic')
    all_subtopics = state.get('subtopics', [])
    previous_summaries = state.get('subtopic_summaries', '')
    
    model = get_model()

    # Get list of all topics and previous summaries
    subtopics_context = "\n".join([f"- {subtopic}" for subtopic in all_subtopics])
    if previous_summaries:
        previous_context = f"Previous subtopics covered:\n{previous_summaries}"
    else:
        previous_context = "This is the first subtopic of the episode."

    # Format the reference document section
    reference_doc = state.get('reference_document', '')
    if reference_doc:
        reference_section = f"Use the following reference document as a guide for content style, examples, and factual information:\n\n{reference_doc}"
    else:
        reference_section = "No reference document provided."

    # Build system prompt for generation with defined contexts
    agent_system_prompt = SystemMessage(SUBTOPIC_GENERATOR_SYSTEM_PROMPT.format(
        podcast_subtopic=subtopic_input,
        podcast_subtopics=subtopics_context,
        previous_subtopics_context=previous_context,
        reference_document_section=reference_section
    ))

    # Invoke with custom system prompt
    messages = [
        agent_system_prompt,
        *state['messages']
    ]
    output = model.invoke(messages)

    # Generate summary of the recently generated content content
    summary_system_prompt = SystemMessage(SUBTOPIC_SUMMARY_SYSTEM_PROMPT.format(
        podcast_subtopic=subtopic_input
    ))
    summary_messages = [
        summary_system_prompt,
        HumanMessage(content=f"Content to summarize:\n\n{output.content}")
    ]
    summary_output = model.invoke(summary_messages)

    # Update state with the new content
    current_subtopic_contents = state.get('subtopic_contents', {})
    current_subtopic_contents[subtopic_input] = output.content
    
    # Append the summary to the subtopic_summaries string
    existing_summaries = state.get('subtopic_summaries', '')
    new_summary = f"\n\n## {subtopic_input}\n{summary_output.content}"
    updated_summaries = existing_summaries + new_summary
    
    return Command(
        goto='subtopic_router_agent',
        update={
            'subtopic_contents': current_subtopic_contents,
            'subtopic_summaries': updated_summaries,
            'completed_subtopics': state.get('completed_subtopics', []) + [subtopic_input]
        }
    )
from langgraph.graph import StateGraph, MessagesState, START, END
from src.llm.agents.subtopic_agent import subtopic_agent
from src.llm.agents.subtopic_router import subtopic_router_agent
from src.llm.agents.subtopic_generator import subtopic_generator_agent
from src.llm.agents.file_writer import filewriter_agent


class CustomState(MessagesState):
    topic: str = 'Unknown'
    subtopics: list[str] = []
    subtopic_contents: dict[str, str] = {}
    completed_subtopics: list[str] = []
    current_subtopic: str
    subtopic_summaries: str
    reference_document: str = ''


def build_graph():
    # Nodes
    builder = StateGraph(state_schema=CustomState)
    builder.add_node('subtopic_agent', subtopic_agent)
    builder.add_node('subtopic_router_agent', subtopic_router_agent)
    builder.add_node('subtopic_generator_agent', subtopic_generator_agent)
    builder.add_node('filewriter_agent', filewriter_agent)

    # Edges
    builder.add_edge(START, 'subtopic_agent')

    graph = builder.compile()
    return graph


graph = build_graph()
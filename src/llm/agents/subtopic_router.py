from langgraph.types import Command
from typing import Literal


def subtopic_router_agent(state) -> Command[Literal['subtopic_generator_agent', 'filewriter_agent']]:
    # Get the subtopics list from state
    subtopics = state.get('subtopics', [])
    completed_subtopics = state.get('completed_subtopics', [])
    
    # Find the next subtopic to process
    remaining_subtopics = [s for s in subtopics if s not in completed_subtopics]
    print(f'Remaining subtopics: {remaining_subtopics}')
    
    if not remaining_subtopics:
        # All subtopics are done, end the workflow
        return Command(goto='filewriter_agent')
    
    # Process the next subtopic
    next_subtopic = remaining_subtopics[0]
    
    return Command(
        goto='subtopic_generator_agent',
        update={
            'current_subtopic': next_subtopic,
            'completed_subtopics': completed_subtopics
        }
    )
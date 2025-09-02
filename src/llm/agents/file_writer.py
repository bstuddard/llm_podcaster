from langgraph.types import Command
from typing import Literal
import json
import os


def filewriter_agent(state) -> Command[Literal['__end__']]:
    # Get the data from state
    topic = state.get('topic', 'Unknown Topic')
    subtopics = state.get('subtopics', [])
    subtopic_contents = state.get('subtopic_contents', {})
    
    # Create output directory if it doesn't exist
    output_dir = "data/text_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Write the list of subtopics in order
    subtopics_file = os.path.join(output_dir, f"{topic.lower().replace(' ', '_')}_subtopics.txt")
    with open(subtopics_file, 'w', encoding='utf-8') as f:
        for i, subtopic in enumerate(subtopics, 1):
            f.write(f"{i}. {subtopic}\n")
    
    # Write each subtopic content to individual files
    subtopic_files = []
    for i, subtopic in enumerate(subtopics, 1):
        if subtopic in subtopic_contents:
            content = subtopic_contents[subtopic]
            filename = f"subtopic_{i:02d}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Write only the raw content, no headers or formatting
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            subtopic_files.append(filename)
    
    # Write a summary JSON file with metadata
    summary_file = os.path.join(output_dir, "summary.json")
    summary_data = {
        "topic": topic,
        "total_subtopics": len(subtopics),
        "subtopics": subtopics,
        "subtopic_files_generated": subtopic_files
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(subtopics)} subtopic files in {output_dir}")
    
    # End the workflow
    return Command(goto='__end__')
import os
import json
from src.startup.load_config import *
from elevenlabs.client import ElevenLabs


api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise ValueError("ELEVENLABS_API_KEY environment variable is not set. Please check your .env file or environment variables.")


def convert_text(text: str = None, input_file_name: str = None, output_file_name: str = "output.mp3"):
    """Convert text to speech and output an MP3 file.
    
    Either provide text directly or specify a text file to read from. The function
    will convert the text to speech using ElevenLabs API and save the audio as an MP3 file.

    Args:
        text (str, optional): Text string to convert to speech. Defaults to None.
        input_file_name (str, optional): Name of text file in data/text_output/ directory to convert. Defaults to None.
        output_file_name (str, optional): Name of the output MP3 file. Defaults to "output.mp3".

    Returns:
        None: Saves the audio file to data/audio_output/ directory.

    Raises:
        ValueError: If both text and input_file_name are provided (only one allowed).
        ValueError: If neither text nor input_file_name is provided.
        FileNotFoundError: If the specified input file is not found in data/text_output/ directory.

    Note:
        - Exactly one of text or input_file_name must be provided
        - Output files are saved to data/audio_output/ directory
        - Uses ElevenLabs text-to-speech API with voice_id "bIHbv24MWmeRgasZH58o"
    """
    # Validate that exactly one input method is provided
    if text is not None and input_file_name is not None:
        raise ValueError("Cannot provide both text and input_file_name. Use one or the other.")
    
    if text is None and input_file_name is None:
        raise ValueError("Must provide either text or input_file_name.")
    
    # If input_file_name is provided, read the text from file
    if input_file_name is not None:
        input_file_path = os.path.join("data", "text_output", input_file_name)
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"Input file not found: {input_file_path}")
        
        with open(input_file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    
    elevenlabs = ElevenLabs(api_key=api_key)

    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="bIHbv24MWmeRgasZH58o",
        model_id="eleven_turbo_v2_5", # or for better quality model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        seed=42
    )

    # Create data directory if it doesn't exist
    data_dir = "data/audio_output"
    os.makedirs(data_dir, exist_ok=True)

    # Save audio to file in data directory
    output_file = os.path.join(data_dir, output_file_name)
    
    # Collect all audio chunks first to ensure complete download
    audio_chunks = []
    for chunk in audio:
        audio_chunks.append(chunk)
    
    # Write the complete audio data
    with open(output_file, "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)
    
    print(f"Audio saved to: {output_file}")


def convert_all_subtopics(summary_file: str = "summary.json"):
    """Convert all subtopics from a summary.json file to MP3 files.
    
    Reads the summary.json file and converts each subtopic text file to an MP3 audio file.
    Output files are named with the subtopic number.

    Args:
        summary_file (str): Path to the summary.json file. Defaults to "summary.json".

    Returns:
        None: Saves MP3 files to data/audio_output/ directory.

    Raises:
        FileNotFoundError: If summary.json or any subtopic text files are not found.
        KeyError: If summary.json is missing required fields.
    """
    # Read the summary file
    summary_path = os.path.join("data", "text_output", summary_file)
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Summary file not found: {summary_path}")
    
    with open(summary_path, 'r', encoding='utf-8') as f:
        summary = json.load(f)
    
    # Extract information from summary
    topic = summary.get('topic', 'unknown_topic')
    subtopic_files = summary.get('subtopic_files_generated', [])
    
    if not subtopic_files:
        print("No subtopic files found in summary file.")
        return
    
    print(f"Converting {len(subtopic_files)} subtopics for topic: {topic}")
    
    # Convert each subtopic file
    for text_file in subtopic_files:
        # Generate output filename (replace .txt with .mp3)
        output_filename = text_file.replace('.txt', '.mp3')
        
        print(f"Converting: {text_file} → {output_filename}")
        
        try:
            # Convert the text file to audio
            convert_text(input_file_name=text_file, output_file_name=output_filename)
            print(f"Completed: {output_filename}")
        except Exception as e:
            print(f"Failed to convert {text_file}: {e}")
    
    print(f"\nBatch conversion complete. Generated {len(subtopic_files)} MP3 files.")


if __name__ == '__main__':
    # Example usage with text
    convert_text(text="The first move is what sets everything in motion.")
    
    # Example usage with file and custom output name
    convert_text(input_file_name="episode_one.txt", output_file_name="episode_one.mp3")
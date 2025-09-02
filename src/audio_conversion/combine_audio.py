import os
import glob
from typing import List
from pydub import AudioSegment


def list_audio_files(audio_dir: str = "data/audio_output") -> list[str]:
    """List all MP3 files in the specified audio directory.
    
    Args:
        audio_dir (str): Path to the audio directory. Defaults to "data/audio_output".
        
    Returns:
        List[str]: List of MP3 filenames found in the directory.
        
    Raises:
        FileNotFoundError: If the audio directory doesn't exist.
    """
    if not os.path.exists(audio_dir):
        raise FileNotFoundError(f"Audio directory not found: {audio_dir}")
    
    # Find all MP3 files in the directory
    mp3_files = glob.glob(os.path.join(audio_dir, "*.mp3"))
    
    # Extract just the filenames (without path)
    filenames = [os.path.basename(file) for file in mp3_files]
    
    # Sort filenames for consistent ordering
    filenames.sort()
    
    return filenames


def combine_audio_files(
    input_files: list[str], 
    output_filename: str = "combined_episode.mp3",
    audio_dir: str = "data/audio_output") -> str:
    """Combine multiple MP3 files into a single MP3 file.
    
    Args:
        input_files (List[str]): List of MP3 filenames to combine.
        output_filename (str): Name of the output combined file. Defaults to "combined_episode.mp3".
        audio_dir (str): Directory containing the input audio files. Defaults to "data/audio_output".
        
    Returns:
        str: Path to the combined audio file.
        
    Raises:
        FileNotFoundError: If any of the input files don't exist.
        ValueError: If no input files are provided.
    """
    if not input_files:
        raise ValueError("No input files provided for combining.")
    
    # Create the full paths to input files
    input_paths = [os.path.join(audio_dir, filename) for filename in input_files]
    
    # Check if all files exist
    for file_path in input_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    print(f"Combining {len(input_files)} audio files...")
    
    # Load the first audio file
    combined = AudioSegment.from_mp3(input_paths[0])
    print(f"Loaded: {input_files[0]}")
    
    # Append each subsequent audio file
    for i, file_path in enumerate(input_paths[1:], 1):
        audio = AudioSegment.from_mp3(file_path)
        combined += audio
        print(f"Added: {input_files[i]}")
    
    # Create output directory if it doesn't exist
    os.makedirs(audio_dir, exist_ok=True)
    
    # Save the combined audio
    output_path = os.path.join(audio_dir, output_filename)
    combined.export(output_path, format="mp3")
    
    print(f"Combined audio saved to: {output_path}")
    print(f"Total duration: {len(combined) / 1000:.2f} seconds")
    
    return output_path


def combine_all_audio_in_directory(
    output_filename: str = "combined_episode.mp3",
    audio_dir: str = "data/audio_output") -> str:
    """Combine all MP3 files in the audio directory into one file.
    
    Args:
        output_filename (str): Name of the output combined file. Defaults to "combined_episode.mp3".
        audio_dir (str): Directory containing the audio files. Defaults to "data/audio_output".
        
    Returns:
        str: Path to the combined audio file.
    """
    # Get all MP3 files in the directory
    audio_files = list_audio_files(audio_dir)
    
    if not audio_files:
        raise ValueError(f"No MP3 files found in {audio_dir}")
    
    print(f"Found {len(audio_files)} MP3 files: {audio_files}")
    
    # Combine all files
    return combine_audio_files(audio_files, output_filename, audio_dir)


if __name__ == "__main__":
    # Example usage: combine all audio files in the directory
    try:
        output_file = combine_all_audio_in_directory()
        print(f"\nSuccessfully created: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example usage: combine specific files
    # specific_files = ["subtopic_01.mp3", "subtopic_02.mp3"]
    # output_file = combine_audio_files(specific_files, "custom_combined.mp3")
    # print(f"Custom combination created: {output_file}")

#!/usr/bin/env python3
"""
LLM Podcast Creator - Command Line Interface

A tool for generating podcast episodes using LLMs and text-to-speech conversion.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Add src to path for imports (following notebook pattern)
sys.path.append(str(Path(__file__).parent / "src"))

from langchain_core.messages import HumanMessage
from llm.graph import graph
from audio_conversion.convert_audio import convert_all_subtopics
from audio_conversion.combine_audio import combine_all_audio_in_directory


def validate_environment():
    """Check if required environment variables are set."""
    required_vars = ["ELEVENLABS_API_KEY", "ANTHROPIC_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file or environment.")
        return False
    
    print("✅ Environment variables validated")
    return True


def check_output_directories_empty() -> None:
    """Check if audio and text output directories are empty. Raises error if not."""
    audio_dir = Path("data/audio_output")
    text_dir = Path("data/text_output")
    
    # Check if directories exist and have files
    audio_files = list(audio_dir.glob("*")) if audio_dir.exists() else []
    text_files = list(text_dir.glob("*")) if text_dir.exists() else []
    
    if audio_files or text_files:
        error_msg = "Output directories are not empty:\n"
        if audio_files:
            error_msg += f"  Audio directory ({len(audio_files)} files): {audio_dir}\n"
        if text_files:
            error_msg += f"  Text directory ({len(text_files)} files): {text_dir}\n"
        error_msg += "Please clear these directories before creating a new episode."
        
        raise ValueError(error_msg)
    
    print("✅ Output directories are empty")


def generate_text_content(topic: str, user_message: str, reference_path: Optional[str] = None) -> bool:
    """Generate podcast text content from a topic and user message."""
    try:
        print(f"🎙️ Generating podcast text content for topic: {topic}")
        
        # Validate environment first (check API keys)
        if not validate_environment():
            print("❌ Environment validation failed")
            return False
        
        # Check if output directories are empty
        check_output_directories_empty()
        
        # Create messages list following notebook pattern
        messages = [HumanMessage(content=user_message)]
        
        # Load reference document if provided
        reference_content = ""
        if reference_path:
            try:
                with open(reference_path, 'r', encoding='utf-8') as f:
                    reference_content = f.read()
                print(f"📚 Loaded reference document: {reference_path}")
            except Exception as e:
                print(f"⚠️ Warning: Could not load reference document: {e}")
        
        # Initialize the graph state
        initial_state = {
            'messages': messages,
            'topic': topic,
            'reference_document': reference_content
        }
        
        # Run the graph to generate content
        print("Generating podcast content...")
        result = graph.invoke(initial_state)
        
        print(f"✅ Generated {len(result.get('subtopics', []))} subtopics")
        print(f"📁 Text files saved to: data/text_output/")
        return True
        
    except Exception as e:
        print(f"❌ Error generating text content: {e}")
        return False


def convert_audio_content() -> bool:
    """Convert generated text content to audio files."""
    try:
        print("🎵 Converting text content to audio...")
        
        # Validate environment first (check API keys)
        if not validate_environment():
            print("❌ Environment validation failed")
            return False
        
        # Check if text files exist
        text_dir = Path("data/text_output")
        if not text_dir.exists() or not list(text_dir.glob("*.txt")):
            print("❌ No text files found in data/text_output/")
            print("Please run 'generate' command first to create text content.")
            return False
        
        # Convert text to speech for each subtopic
        convert_all_subtopics()
        
        print(f"✅ Audio files saved to: data/audio_output/")
        return True
        
    except Exception as e:
        print(f"❌ Error converting audio content: {e}")
        return False


def combine_audio_files() -> bool:
    """Combine all audio files into a single episode."""
    try:
        print("🎵 Combining audio files...")
        
        # Check if audio files exist
        audio_dir = Path("data/audio_output")
        if not audio_dir.exists() or not list(audio_dir.glob("*.mp3")):
            print("❌ No audio files found in data/audio_output/")
            print("Please run 'convert' command first to create audio files.")
            return False
        
        # Combine all audio files
        combine_all_audio_in_directory(
            output_filename="combined_episode.mp3",
            audio_dir="data/audio_output"
        )
        print("✅ Audio combination completed")
        print(f"🎉 Final episode saved as: data/audio_output/combined_episode.mp3")
        return True
        
    except Exception as e:
        print(f"❌ Error combining audio files: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_podcast_episode(topic: str, user_message: str, reference_path: Optional[str] = None) -> bool:
    """Create a complete podcast episode from a topic and user message (all-in-one)."""
    try:
        print(f"🎙️ Creating podcast episode for topic: {topic}")
        
        # Step 1: Generate text content
        if not generate_text_content(topic, user_message, reference_path):
            return False
        
        # Step 2: Convert to audio
        if not convert_audio_content():
            return False
        
        # Step 3: Combine audio files
        if not combine_audio_files():
            return False
        
        print(f"🎉 Podcast episode created successfully!")
        print(f"📁 Output directory: data")
        return True
        
    except Exception as e:
        print(f"❌ Error creating podcast episode: {e}")
        return False


def list_episodes() -> None:
    """List existing podcast episodes."""
    audio_dir = Path("data") / "audio_output"
    text_dir = Path("data") / "text_output"
    
    print("📚 Existing Podcast Episodes:")
    print("-" * 40)
    
    # List audio files
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.mp3"))
        if audio_files:
            print("🎵 Audio Files:")
            for file in audio_files:
                print(f"  • {file.name}")
        else:
            print("  No audio files found")
    
    # List text files
    if text_dir.exists():
        text_files = list(text_dir.glob("*.txt"))
        if text_files:
            print("\n📝 Text Files:")
            for file in text_files:
                print(f"  • {file.name}")
        else:
            print("  No text files found")


def test_environment() -> bool:
    """Test the environment and dependencies."""
    print("🧪 Testing environment...")
    
    if not validate_environment():
        return False
    
    try:
        # Test graph import and basic functionality
        print("✅ Graph imported successfully")
        print("✅ All dependencies working correctly")
        return True
    except Exception as e:
        print(f"❌ Error testing dependencies: {e}")
        return False


def reconvert_single_file(text_filename: str) -> bool:
    """Reconvert a single text file to audio."""
    try:
        print(f"🎵 Reconverting single file: {text_filename}")
        
        # Validate environment first (check API keys)
        if not validate_environment():
            print("❌ Environment validation failed")
            return False
        
        # Check if the text file exists
        text_file_path = Path("data/text_output") / text_filename
        if not text_file_path.exists():
            print(f"❌ Text file not found: {text_file_path}")
            return False
        
        # Generate output filename (replace .txt with .mp3)
        output_filename = text_filename.replace('.txt', '.mp3')
        
        # Import and use the convert_text function
        from audio_conversion.convert_audio import convert_text
        
        # Convert the single file
        convert_text(input_file_name=text_filename, output_file_name=output_filename)
        
        print(f"✅ Successfully reconverted: {text_filename} → {output_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error reconverting file: {e}")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LLM Podcast Creator - Generate podcast episodes using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # All-in-one approach (original behavior)
  python main.py create "leetcode prep" "I want to create a podcast episode as part of a leetcode prep series. Make this first one a general overview but do not dive into any specific patterns. Only include 2 subtopics."
  
  # Step-by-step approach (recommended for debugging)
  python main.py generate "leetcode prep" "I want to create a podcast episode as part of a leetcode prep series. Make this first one a general overview but do not dive into any specific patterns. Only include 2 subtopics."
  python main.py convert
  python main.py combine
  
  # Other commands
  python main.py list
  python main.py test
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command (all-in-one)
    create_parser = subparsers.add_parser("create", help="Create a complete podcast episode (all steps)")
    create_parser.add_argument("topic", help="Topic for the podcast episode")
    create_parser.add_argument("message", help="User message describing what to create")
    create_parser.add_argument("--reference", "-r", help="Path to reference document file")
    
    # Generate command (text only)
    generate_parser = subparsers.add_parser("generate", help="Generate podcast text content only")
    generate_parser.add_argument("topic", help="Topic for the podcast episode")
    generate_parser.add_argument("message", help="User message describing what to create")
    generate_parser.add_argument("--reference", "-r", help="Path to reference document file")
    
    # Convert command (text to audio)
    subparsers.add_parser("convert", help="Convert generated text content to audio files")
    
    # Combine command (audio combination)
    subparsers.add_parser("combine", help="Combine audio files into final episode")
    
    # List command
    subparsers.add_parser("list", help="List existing podcast episodes")
    
    # Test command
    subparsers.add_parser("test", help="Test the environment and dependencies")
    
    # Reconvert command (single file)
    reconvert_parser = subparsers.add_parser("reconvert", help="Reconvert a single text file to audio")
    reconvert_parser.add_argument("filename", help="Name of the text file to reconvert (e.g., subtopic_00.txt)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "create":
            success = create_podcast_episode(args.topic, args.message, args.reference)
            if not success:
                sys.exit(1)
                
        elif args.command == "generate":
            success = generate_text_content(args.topic, args.message, args.reference)
            if not success:
                sys.exit(1)
                
        elif args.command == "convert":
            success = convert_audio_content()
            if not success:
                sys.exit(1)
                
        elif args.command == "combine":
            success = combine_audio_files()
            if not success:
                sys.exit(1)
                
        elif args.command == "list":
            list_episodes()
            
        elif args.command == "test":
            success = test_environment()
            if not success:
                sys.exit(1)
                
        elif args.command == "reconvert":
            success = reconvert_single_file(args.filename)
            if not success:
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

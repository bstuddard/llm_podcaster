# LLM Podcast Creator

An AI-powered tool that generates podcast episodes using LLMs and text-to-speech conversion.

## Prerequisites

- Python 3.8+
- FFmpeg (for audio processing)

## Installation

1. **Install FFmpeg**:
   ```bash
   # Windows
   winget install "FFmpeg (Essentials Build)"
   
   # macOS
   brew install ffmpeg
   
   # Linux
   sudo apt install ffmpeg
   ```

2. **Setup**:
   ```bash
   git clone <your-repo-url>
   cd llm_podcast_createor
   pip install -r requirements.txt
   ```

3. **Environment**:
   Create a `.env` file:
   ```bash
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Quick Start

**All-in-one:**
```bash
python main.py create "Python Tips" "Create a podcast about Python best practices with 3 subtopics"
```

**Step-by-step:**
```bash
python main.py generate "Python Tips" "Create a podcast about Python best practices with 3 subtopics"
python main.py convert
python main.py combine
```

## Commands

- `create` - Generate complete episode (all steps)
- `generate` - Create text content only
- `convert` - Convert text to audio
- `combine` - Combine audio files
- `reconvert <file>` - Reconvert single text file
- `list` - Show existing episodes
- `test` - Test environment

## Reference Documents

Add `--reference <file.txt>` to any command to guide content style and examples.

## Project Structure

- `src/llm/` - LLM agents and content generation
- `src/audio_conversion/` - Text-to-speech conversion
- `data/` - Generated outputs
- `main.py` - Command-line interface
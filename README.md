# Stream Transcriber

A Python application that can listen to YouTube videos or livestreams and transcribe the audio content, saving the results as Word documents.

## Features

- 🎥 Extract audio from YouTube videos and livestreams
- 🎵 Convert audio to text using Google Speech Recognition
- 📄 Save transcriptions as Word documents (.docx)
- 🌐 Web-based interface using Streamlit
- ⚡ Fast and efficient processing

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
streamlit run main.py
```

2. Open your web browser and navigate to the Streamlit interface
3. Enter a YouTube URL (video or livestream)
4. Click "Transcribe" to start the process
5. Download the generated Word document

## Requirements

- Python 3.7+
- Internet connection (for Google Speech Recognition)
- FFmpeg (for audio processing)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## How It Works

1. **Audio Extraction**: Uses `yt-dlp` to download audio from YouTube videos
2. **Audio Processing**: Converts audio to WAV format using `pydub`
3. **Speech Recognition**: Transcribes audio using Google's Speech Recognition API
4. **Document Generation**: Creates Word documents using `python-docx`

## Supported Formats

- YouTube videos (all formats)
- YouTube livestreams
- Various audio formats (automatically converted)

## Limitations

- Requires internet connection for speech recognition
- Audio quality affects transcription accuracy
- Processing time depends on video length
- Google Speech Recognition has usage limits

## Troubleshooting

### Common Issues

1. **"Could not understand the audio"**
   - Try a video with clearer audio
   - Check if the video has speech content

2. **"Error extracting audio"**
   - Verify the YouTube URL is correct
   - Check internet connection
   - Ensure FFmpeg is installed

3. **"Error with speech recognition service"**
   - Check internet connection
   - Google's service might be temporarily unavailable

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

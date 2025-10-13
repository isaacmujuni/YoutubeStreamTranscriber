# Contributing to YouTube Stream Transcriber

Thank you for your interest in contributing to this project! Here are some guidelines to help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Install dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.7+
- FFmpeg installed
- Git

### Installation
```bash
git clone https://github.com/isaacmujuni/YoutubeStreamTranscriber.git
cd YoutubeStreamTranscriber
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run main.py
```

## Areas for Contribution

### Features
- [ ] Support for other video platforms (Vimeo, Twitch, etc.)
- [ ] Batch processing of multiple URLs
- [ ] Real-time transcription for livestreams
- [ ] Export to other formats (PDF, TXT, SRT)
- [ ] Speaker identification and separation
- [ ] Language detection and auto-selection
- [ ] Custom vocabulary support
- [ ] Audio quality enhancement

### Improvements
- [ ] Better error handling and recovery
- [ ] Progress bars for long operations
- [ ] Configuration file support
- [ ] Docker containerization
- [ ] API endpoints for programmatic access
- [ ] Performance optimizations
- [ ] Better UI/UX design
- [ ] Mobile responsiveness

### Documentation
- [ ] API documentation
- [ ] Video tutorials
- [ ] Troubleshooting guide
- [ ] Performance benchmarks
- [ ] Deployment guides

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Include type hints where appropriate
- Write clear commit messages

## Testing

Before submitting a pull request:
1. Test with different YouTube URLs
2. Test with various audio qualities
3. Test error scenarios
4. Ensure the UI works properly

## Submitting Changes

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes
3. Commit with descriptive messages
4. Push to your fork
5. Create a pull request

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Error messages
- Steps to reproduce
- Sample URLs (if applicable)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

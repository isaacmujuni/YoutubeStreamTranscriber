import streamlit as st
import yt_dlp
import speech_recognition as sr
from pydub import AudioSegment
from docx import Document
import tempfile
import os
import threading
import time
from datetime import datetime
import whisper
import torch

class StreamTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.transcription_text = ""
        self.whisper_model = None
        
    def load_whisper_model(self, model_size="tiny"):
        """Load OpenAI Whisper model"""
        try:
            if self.whisper_model is None:
                with st.spinner(f"Loading Whisper {model_size} model (this may take a few minutes on first run)..."):
                    self.whisper_model = whisper.load_model(model_size)
            return True
        except Exception as e:
            st.error(f"Error loading Whisper model: {str(e)}")
            return False
        
    def extract_audio_from_youtube(self, url):
        """Extract audio from YouTube video/livestream"""
        try:
            # Create temporary directory for download
            temp_dir = tempfile.mkdtemp()
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First get info to extract title
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                
                # Clean title for filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                
                # Download the audio
                ydl.download([url])
                
                # Find the downloaded file
                downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith(('.wav', '.webm', '.m4a', '.mp3', '.ogg'))]
                if downloaded_files:
                    audio_file = os.path.join(temp_dir, downloaded_files[0])
                    return title, audio_file
                else:
                    st.error("No audio file was downloaded")
                    return None, None
                
        except Exception as e:
            st.error(f"Error extracting audio: {str(e)}")
            return None, None
    
    def transcribe_audio_file(self, audio_file_path, use_whisper=True, model_size="tiny"):
        """Transcribe audio file to text using OpenAI Whisper or Google Speech Recognition"""
        try:
            if use_whisper:
                return self.transcribe_with_whisper(audio_file_path, model_size)
            else:
                return self.transcribe_with_google(audio_file_path)
        except Exception as e:
            st.error(f"Error transcribing audio: {str(e)}")
            return ""
    
    def transcribe_with_whisper(self, audio_file_path, model_size="tiny"):
        """Transcribe using OpenAI Whisper"""
        try:
            # Load Whisper model
            if not self.load_whisper_model(model_size):
                return ""
            
            # Transcribe with Whisper
            with st.spinner("Transcribing with OpenAI Whisper..."):
                result = self.whisper_model.transcribe(audio_file_path)
                return result["text"]
                
        except Exception as e:
            st.error(f"Error with Whisper transcription: {str(e)}")
            return ""
    
    def transcribe_with_google(self, audio_file_path):
        """Transcribe using Google Speech Recognition (fallback)"""
        try:
            # Load audio file
            audio = AudioSegment.from_file(audio_file_path)
            
            # Convert to WAV format with proper settings for speech recognition
            wav_path = audio_file_path.rsplit('.', 1)[0] + '.wav'
            audio = audio.set_frame_rate(16000).set_channels(1)  # Mono, 16kHz for better recognition
            audio.export(wav_path, format="wav")
            
            # Use speech recognition
            with sr.AudioFile(wav_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                audio_data = self.recognizer.record(source)
                
            # Transcribe using Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data)
            return text
            
        except sr.UnknownValueError:
            st.error("Could not understand the audio")
            return ""
        except sr.RequestError as e:
            st.error(f"Error with speech recognition service: {e}")
            return ""
        except Exception as e:
            st.error(f"Error transcribing audio: {str(e)}")
            return ""
    
    def save_to_word_document(self, text, title, output_path):
        """Save transcribed text to Word document"""
        try:
            doc = Document()
            doc.add_heading(f'Transcription: {title}', 0)
            doc.add_paragraph(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            doc.add_paragraph()
            
            # Split text into paragraphs for better formatting
            paragraphs = text.split('. ')
            for paragraph in paragraphs:
                if paragraph.strip():
                    doc.add_paragraph(paragraph.strip() + '.')
            
            doc.save(output_path)
            return True
            
        except Exception as e:
            st.error(f"Error saving Word document: {str(e)}")
            return False
    
    def process_youtube_url(self, url, use_whisper=True, model_size="tiny"):
        """Main method to process YouTube URL and create transcription"""
        with st.spinner("Extracting audio from YouTube..."):
            title, audio_file = self.extract_audio_from_youtube(url)
            
        if not title or not audio_file:
            return False
            
        with st.spinner("Transcribing audio..."):
            transcription = self.transcribe_audio_file(audio_file, use_whisper, model_size)
            
        if not transcription:
            return False
            
        # Save to Word document
        output_filename = f"{title.replace(' ', '_')}_transcription.docx"
        output_path = os.path.join(os.getcwd(), output_filename)
        
        with st.spinner("Saving to Word document..."):
            success = self.save_to_word_document(transcription, title, output_path)
            
        if success:
            st.success(f"Transcription saved as: {output_filename}")
            return True
        else:
            return False

def main():
    st.set_page_config(
        page_title="Stream Transcriber",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 Stream Transcriber")
    st.markdown("Transcribe YouTube videos and livestreams to Word documents")
    
    transcriber = StreamTranscriber()
    
    # Input section
    st.header("📝 Enter YouTube URL")
    url = st.text_input("YouTube Video or Livestream URL:", placeholder="https://www.youtube.com/watch?v=...")
    
    # Advanced options
    st.header("⚙️ Transcription Options")
    col1, col2 = st.columns(2)
    
    with col1:
        use_whisper = st.checkbox("Use OpenAI Whisper (Recommended)", value=True, 
                                 help="Better accuracy and supports multiple languages")
    
    with col2:
        if use_whisper:
            model_size = st.selectbox("Whisper Model Size", 
                                    ["tiny", "base", "small", "medium", "large"],
                                    index=0,
                                    help="Larger models = better accuracy but slower processing")
        else:
            model_size = "tiny"  # Not used for Google Speech Recognition
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        transcribe_button = st.button("🎯 Transcribe", type="primary")
    
    with col2:
        if transcribe_button and url:
            if transcriber.process_youtube_url(url, use_whisper, model_size):
                st.balloons()
            else:
                st.error("Transcription failed. Please check the URL and try again.")
    
    # Instructions
    st.header("📋 How to Use")
    st.markdown("""
    1. **Copy a YouTube URL** - Paste any YouTube video or livestream URL
    2. **Choose transcription method** - Select OpenAI Whisper (recommended) or Google Speech Recognition
    3. **Click Transcribe** - The app will extract audio and transcribe it
    4. **Download** - Get your Word document with the transcription
    
    **Note:** OpenAI Whisper works offline after initial model download. Google Speech Recognition requires internet.
    """)
    
    # Features
    st.header("✨ Features")
    st.markdown("""
    - 🎥 **YouTube Support** - Works with videos and livestreams
    - 🎵 **Audio Extraction** - Automatically extracts audio from video
    - 🤖 **OpenAI Whisper** - State-of-the-art speech recognition with multi-language support
    - 🌐 **Google Speech Recognition** - Fallback option requiring internet connection
    - 📄 **Word Documents** - Saves transcriptions in .docx format
    - ⚡ **Fast Processing** - Quick transcription and document generation
    - 🔧 **Model Selection** - Choose Whisper model size based on accuracy vs speed needs
    """)

if __name__ == "__main__":
    main()

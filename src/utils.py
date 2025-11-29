import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import os
import sys
from ctypes import *
from contextlib import contextmanager

# Define error handler to suppress ALSA warnings
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    try:
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield

# Initialize pygame mixer for audio playback
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Error initializing pygame mixer: {e}")

# Voice setting: British Male (Closest to Iron Man's Jarvis in free tier)
VOICE = "en-GB-RyanNeural"
OUTPUT_FILE = "response.mp3"

async def _generate_audio(text):
    """Generates MP3 audio from text using Edge TTS."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

def speak(text):
    """Converts text to speech using Edge TTS and plays it."""
    try:
        # Generate the audio file
        asyncio.run(_generate_audio(text))
        
        # Play the audio file
        if os.path.exists(OUTPUT_FILE):
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
            
            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Unload the file so it can be deleted/overwritten
            pygame.mixer.music.unload()
            # Optional: os.remove(OUTPUT_FILE) to clean up
            
    except Exception as e:
        print(f"Error in TTS: {e}")

def listen():
    """Listens to the microphone and returns the recognized text."""
    r = sr.Recognizer()
    
    # Suppress ALSA errors during microphone initialization
    with noalsaerr():
        try:
            source = sr.Microphone()
            with source:
                print("Listening...")
                r.adjust_for_ambient_noise(source)
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    print("Recognizing...")
                    query = r.recognize_google(audio, language='en-US')
                    print(f"User said: {query}\n")
                    return query.lower()
                except sr.WaitTimeoutError:
                    return None
                except sr.UnknownValueError:
                    return None
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return None
        except Exception as e:
            print(f"Microphone error: {e}")
            return None

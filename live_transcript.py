import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import voice_commands


transcript_file = open('transcript.txt', 'a', encoding='utf-8', buffering=1)
print()

def live_transcribe():
    # Define the model path (change this to the path where you downloaded the model)
    model_path = 'D:/projects/examples/voice recognition/farsi_stt' # Adjust path as needed

    # Check if the model exists
    if not os.path.exists(model_path):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    # Load the Vosk model
    print("Loading Vosk model...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)  # Model and sample rate

    # Initialize PyAudio
    print("Initializing PyAudio...")
    audio = pyaudio.PyAudio()

    # Attempt to open the microphone stream
    try:
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
        stream.start_stream()
        print("Microphone stream started. Listening...")

        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                # Print the result of recognition
                result = recognizer.Result()
                text = json.loads(result)["text"]
                if text != "":
                    transcript_file.write(text + '\n')
                    transcript_file.flush()
                os.fsync(transcript_file.fileno())
                print(f"Transcription: {text}")
            else:
                # Print live recognition
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result)["partial"]
                if partial_text:
                    print(f"Partial: {partial_text}", end='\r')

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up the audio stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        transcript_file.close()
        print("Microphone stream closed.")

if __name__ == "__main__":
    live_transcribe()

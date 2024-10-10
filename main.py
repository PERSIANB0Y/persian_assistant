import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from pyfirmata import Arduino, util, OUTPUT
import pyttsx3

print("app is starting.")
print("please wait...")

commands = {
    "bluelightoff": ["چراغ", "آبی", "خاموش"],
    "bluelighton": ["چراغ", "آبی", "روشن"],
    "redlightoff": ["چراغ", "قرمز", "خاموش"],
    "redlighton": ["چراغ", "قرمز", "روشن"],
    "whitelightoff": ["چراغ", "سفید", "خاموش"],
    "whitelighton": ["چراغ", "سفید", "روشن"]
}
board = Arduino('COM11')
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0") #female
transcript_file = open('transcript.txt', 'a', encoding='utf-8', buffering=1)
model_path = 'D:/projects/examples/voice recognition/farsi_stt' # Adjust path as needed
for pin in range(2, 14):
    board.digital[pin].mode = OUTPUT
    board.digital[pin].write(0)
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

try:
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()
    print("Microphone stream started. ")
    print("Listening...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            # Print the result of recognition
            result = recognizer.Result()
            text = json.loads(result)["text"]
            if text != "":
                print(text)
                transcript_file.write(text + '\n')
                transcript_file.flush()
                os.fsync(transcript_file.fileno())
                
                user_words = text.split()

                for command_name, command_words in commands.items():
                    print(command_name, command_words)
                    if all(word in user_words for word in command_words):
                        print("mached")
                        if command_name == "bluelightoff":
                            board.digital[13].write(0)
                            engine.say("blue light turned off")
                        if command_name == "bluelighton":
                            board.digital[13].write(1)
                            engine.say("blue light turned on")
                        
                        engine.runAndWait()
                        engine.stop()



except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    transcript_file.close()
    print("Microphone stream closed.")

import pyttsx3

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set properties (you can adjust volume and rate as needed)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
    
    # Use Persian voice if available
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'fa' in voice.languages:
            engine.setProperty('voice', voice.id)
            break
    
    # Speak the text
    engine.say(text)
    engine.runAndWait()

# Example usage
persian_text = "hello world"
text_to_speech(persian_text)

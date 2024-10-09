from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

basepath="/train_output/run-December-24-2022_09+28AM-0000000"
config=basepath+"/config.json" 
model=basepath+"/best_model.pth"

model_path =model # Absolute path to the model checkpoint.pth
config_path =config # Absolute path to the model config.json

text=".زندگی فقط یک بار است؛ از آن به خوبی استفاده کن"

synthesizer = Synthesizer(
    model_path, config_path
)
wavs = synthesizer.tts(text)
synthesizer.save_wav(wavs, 'sp.wav')

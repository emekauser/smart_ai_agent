from agent.transcribe.speech_to_text import transcribe_short_audio, transcribe_audio
from agent.agents.text_correction_agent import correct_text

text = transcribe_short_audio("data/audio_2025-09-11_18-25-26.wav")
print(text)
text_2 = correct_text(text)
print(text_2)

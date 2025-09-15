
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

# from ..agents.text_correction_agent import correct_text

recognizer = sr.Recognizer()


def transcribe_short_audio(file_path: str) -> str:
    audio = AudioSegment.from_file(file_path, format="ogg")
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}")

    return ""


def transcribe_audio(file_path: str) -> str:
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

    # Split audio into chunks based on silence
    chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-40)

    transcript = ""
    for i, chunk in enumerate(chunks):
        chunk.export("chunk.wav", format="wav")
        with sr.AudioFile("chunk.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                transcript += f"{text} "
            except sr.UnknownValueError:
                print(f"Could not understand audio chunk {i}")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}")

    return transcript.strip()


def ogg_to_wav(input_ogg_path, output_wav_path):
    """
    Converts an OGG audio file to WAV format.

    Args:
        input_ogg_path (str): The path to the input OGG file.
        output_wav_path (str): The path where the output WAV file will be saved.
    """
    try:
        # Load the OGG file
        audio = AudioSegment.from_file(input_ogg_path, format="ogg")

        # Export as WAV
        audio.export(output_wav_path, format="wav")
        print(
            f"Successfully converted '{input_ogg_path}' to '{output_wav_path}'")
    except Exception as e:
        print(f"Error converting OGG to WAV: {e}")


# print(ogg_to_wav("data/audio_2025-09-11_18-25-26.ogg",
#       "data/audio_2025-09-11_18-25-26.wav"))
# text = transcribe_short_audio("data/audio_2025-09-11_18-25-26.wav")
# print(text)
# text_2 = correct_text(text)
# print(text_2)

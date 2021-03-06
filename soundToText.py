
# source: https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python


# ffmpeg -i PTT-20200728-WA0008.opus newfilename.wav

import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import glob

import speech_recognition as sr

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language="es-ES")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text + "\n"
    # return the text for all chunks detected
    return whole_text

r = sr.Recognizer()


path = '/home/sp81891/PycharmProjects/pysound/audio'
files = [f for f in glob.glob(path + "/*.wav", recursive=True)]
for f in files:
    print("------------------------------------------------------------------------------")
    print(f)
    print("------------------------------------------------------------------------------")
    result = get_large_audio_transcription(f)
    print("\nFull text:", result)
    print("")
    text_file = open("texto/"+os.path.basename(f)+".txt", "w")
    text_file.write(result)
    text_file.close()    
from utils.constants import *
import os
import numpy as np
import essentia.standard as estd

def load_dataset():
    """Gets all wav files in the WAV_FOLDER and returns a list of the names.
    
    Args:
        dataset_path: relative path to the root directory

    Returns:
        list containing all file names with no extension
    """

    files = [f for f in os.listdir(WAV_FOLDER) if f.endswith('.wav')]

    for i,file in enumerate(files):

        name, _ = os.path.splitext(file)
        files[i] = name

    return sorted(files)

def load_file(filename: str, sr=SAMPLE_RATE):
    """Gets the audio information of filename.wav in WAV_FOLDER and applies an equal loudness filter.

    Args:
        filename: name of trhe file to extract without extension
        sr: sample rate
    
    Returns:
        audio: audio information for that file
    """

    audio_path = os.path.join(WAV_FOLDER, filename + ".wav")

    return estd.EqloudLoader(filename=audio_path, sampleRate=sr)()

def save_pitch(pitch: list, filename: str):
    """Stores the pitch list in a filename.csv file in EXT_CSV_FOLDER.
    
    Args:
        pitch: iterable with the main pitch per each frame
        filename: name of trhe file to extract without extension
      
    Returns:
        audio: audio information for that file
    """

    if filename == "": raise ValueError("filename required")
    if len(pitch) == 0: raise ValueError("Pitch array empty!")

    ms = np.round(np.arange(len(pitch))*HOP_SIZE/SAMPLE_RATE,decimals=3)

    with open(os.path.join(EXT_CSV_FOLDER,filename + "EXT.txt"),'w') as txtfile:
        for c1,c2 in zip(ms,pitch):
            
            txtfile.write("{:.3f}".format(c1)+"     " +
                          "{:.3f}".format(c2) + "\n")


from utils.constants import *
from utils.utils import *
import essentia.standard as estd

def mpd(audio, frameSize=ANALYZE_SOUND_FRAME_SIZE, hopSize=HOP_SIZE):
    """
    
    Args:
        audio: list with audio samples

    Kwargs:
        frameSize: int with the frame_size to consider when doing pitch predicition
        hopSize: int with the hop_size to consider when doing pitch predicition

    Returns:
        frame_freq: a list where each position is a list containing the possible frequencies for each frame
    """

    # Getting the window
    window = estd.Windowing()

    # List of frequencies for each frame in a list
    frame_freq = []

    # For each frame in the audio file
    for frame in estd.FrameGenerator(audio, frameSize=frameSize, hopSize=hopSize):

        frame_win = window(frame)

        # Computing the autocorrelation
        AC, f0 = autocorrelation(frame_win)
        
        #Normalizing Autocorrelation function
        AC = AC/max(AC)

        # Getting the peaks
        framelist,_ = get_peaks(AC, f0)

        #Add frame to matrix
        frame_freq.append(framelist)

    # Returning the list
    return frame_freq

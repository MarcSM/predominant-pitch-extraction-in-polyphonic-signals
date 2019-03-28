from utils.constants import *
from utils.utils import *

def mptc(audio_multi_pitch):
    """Computes the Multi Pitch Trajection (MPTC) algorithm for the given signal
    
    Args:
        audio_multi_pitch: numpy.array of sorted frequencies by relevance for each frame
        
    Returns:
        freq_arr: numpy.array of the corrected pitch trajectory
    """

    # FRAME LENGTH REDUCTION
    audio_multi_pitch = framesReduction(audio_multi_pitch)

    #GET THE MOST LIKELY FREQUENCY VALUE
    most_likely_freq_arr = getMostLikely(audio_multi_pitch)

    # OCTAVE CORRECTION
    freq_arr = octaveCorrection(most_likely_freq_arr)

    return freq_arr

def getMostLikely(freq_mat):
    """Returns the most likely frequency for each frame and contructs only one list with them.

    Args:
        freq_mat: numpy.array of sorted frequencies by relevance for each frame
        
    Returns:
        numpy.array of the most likely pitch trajectory.
    """

    most_likely_freq_arr = []

    for frame in freq_mat:

        if frame:
            most_likely_freq_arr.append(frame[0])
        else:
            most_likely_freq_arr.append(0)

    return most_likely_freq_arr

    #return [frame[0] for frame in freq_mat if frame]

def octaveCorrection(freq_arr, tol_percent=TOL_PERCENT):
    """Corrects errors of an octave shift from frame to frame.
    
    Args:
        freq_arr: numpy.array of the pitch trajectory
        tol_percent: Tolerance percentage allowed as error when detecting octaves

    Returns:
        freq_arr: numpy.array of the corrected pitch trajectory
    """

    if tol_percent > 100:
        raise ValueError("tol_percent music be 0 < tol_percent <= 100")
    elif tol_percent <= 0:
        raise ValueError("tol_percent music be 0 < tol_percent <= 100")

    octave_ratio = 2
    inverse_octave_ratio = 1/octave_ratio
    tolerance = tol_percent/100

    for i, freq in enumerate(freq_arr):
        if i < len(freq_arr)-1:
            if freq_arr[i+1] == 0: ratio = 0 
            else: ratio = freq/freq_arr[i+1]
            if (1-tolerance)*octave_ratio < ratio < (1+tolerance)*octave_ratio:
                freq_arr[i+1] = octave_ratio * freq_arr[i+1]
            elif (1-tolerance)*inverse_octave_ratio < ratio < (1+tolerance)*inverse_octave_ratio:
                freq_arr[i+1] = freq_arr[i+1] / octave_ratio

    return freq_arr

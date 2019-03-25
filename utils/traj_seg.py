from utils.constants import *
from utils.utils import *
import numpy as np
import essentia.standard as estd


def trajectory_segmentation(audio, freq_arr, frameSize=ANALYZE_SOUND_FRAME_SIZE, hopSize=HOP_SIZE):
    """Creates and applies masks to the frequency array
    
    Args:
        audio: numpy.array of the audio file
        freq_arr: numpy.array of the most likely frequency for each frame
        frameSize: size of the frame for extracting features
        hopSize: hop size of the frame for extracting features
        
    Returns:
        freq_arr_masked : numpy.array of frequencies per frame with applied masks
    """

    # Computing the energy mask
    energy_mask = compute_energy_mask(audio)

    # Computing the frequency derivative mask
    freq_diff_mask = compute_freq_diff_mask(freq_arr)

    # Applying the masks to the frequency array
    freq_arr_masked = apply_masks(freq_arr, energy_mask, freq_diff_mask)

    # Returning the masked frequency array
    return freq_arr_masked

def compute_energy_mask(audio, energy_threshold=ENERGY_THRESHOLD, frameSize=ANALYZE_SOUND_FRAME_SIZE, hopSize=HOP_SIZE):
    """Computes the energy per frame of the signal and generates a mask array for the given signal
    
    Args:
        audio: numpy.array Audio file
        energy_threshold: ammount over one for which the energy is assumed null
        frameSize: size of the frame for extracting features
        hopSize: hop size of the frame for extracting features 
        
    Returns:
        energy_mask: enery mask (boolean array of True = 1 and False = 0)
    """

    #Energy computation
    energy = compute_energy(audio, frameSize=frameSize, hopSize=hopSize)
    
    #Function smoothing
    energy = smooth_function(
        energy, window_type='triang', window_len=50, mode='same')

    # Computing the energy mask
    energy_mask = apply_threshold(energy, energy_threshold)

    # Returning the energy mask
    return energy_mask

def compute_energy(audio, frameSize=ANALYZE_SOUND_FRAME_SIZE, hopSize=HOP_SIZE):
    """Frame based Computation of the energy for a given signal
    
    Args:
        audio: numpy.array of the audio signal

    Returns:
        energy: numpy.array of the enery for each frame
    """

    # Getting the window
    window = estd.Windowing()

    # Energy array
    energy = []

    # For each frame in the audio file
    for frame in estd.FrameGenerator(audio, frameSize=frameSize, hopSize=hopSize):

        frame_win = window(frame)

        energy.append(np.sum(frame_win**2) / len(frame))

    return np.array(energy)

def compute_freq_diff_mask(freq_arr, midi_th=MIDI_TH):
    '''Computes the frequency derivative of a frequency array and generates a mask array for the given signal
    Parameters
    ----------
    freq_arr : numpy.array
        Frequency array
        
    Returns
    -------
    midi_diff_val_mask : numpy.array
        Frequency derivative mask
    '''

    #compute the midi values from the frequencies
    midi = freq2MIDI(freq_arr)

    #compute the derivative
    midi_diff = abs(np.diff(midi))
    midi_diff = np.append(midi_diff, 0)

    #Apply threshold
    midi_diff = apply_threshold(midi_diff, midi_th)

    #smoothen
    midi_diff = smooth_function(
        midi_diff, window_type='hann', window_len=60, mode='same')

    #Apply threshold
    midi_diff = apply_threshold(midi_diff, midi_th)

    # Returning the frequency derivative mask
    return 1 - midi_diff

import numpy as np
from utils.constants import *
from scipy import signal

def autocorrelation(x_win, sr=SAMPLE_RATE, minF0=MIN_F0, maxF0=MAX_F0):
    """F0 detection on a single frame using autocorrelation
    
    Args:
        x_win: numpy.array of the windowed signal frame
        fs: Sampling rate
        minF0: Min F0 limit
        maxF0: Max F0 limit
        
    Returns:
        ValAC: numpy.array of the autocorrelation values.
        f0: numpy.array f values for those ValAC values
    """
    f0 = np.array([])
    minT0 = int(np.round(sr/maxF0))
    maxT0 = int(np.round(sr/minF0))

    Ts = range(minT0, maxT0)
    ValAC = np.array([])

    for k in Ts:
        x_win_shifted = np.hstack((np.zeros(k), x_win[:-k]))
        autoCorr = np.dot(x_win, x_win_shifted)
        ValAC = np.append(ValAC, autoCorr)

    f0 = np.divide(sr*np.ones(len(Ts)), Ts)
    return ValAC, f0

def get_peaks(sig:list, xticks:list):
    """Returns the x,y values of the peaks in sig

    Args:
        sig: numpy.array of the signal of which to fing the peaks
        xticks: numpy.array of the corresponding x axis values for sig

    Returns:
        yval: y values of the peaks
        xval: x values of the peaks
    """

    if len(sig) != len(xticks):
        raise ValueError("xticks and sig must have the same length")

    peaks, _ = signal.find_peaks(sig)

    tuplelist = [(a, b) for a, b in zip(xticks[peaks], sig[peaks])]
    tuplelist.sort(key=lambda x: x[1], reverse=True)

    yval = [a for a, b in tuplelist]
    xval = [b for a, b in tuplelist]

    return yval, xval

def framesReduction(frames_mat):
    """Modifies frames_mat to only contain the three first elements in each element

    Args:
        frames_mat: list of frames

    Returns:
        frames_mat: modified list of frames
    """

    for i, frame in enumerate(frames_mat):

        upper = min(3, len(frame))
        frames_mat[i] = frame[:upper]

    return frames_mat

def smooth_function(sig, window_type= 'triang', window_len = 50, mode = 'same'):
    return np.convolve(sig, signal.get_window(window_type, window_len), mode=mode)

def apply_threshold(sig,th):
    """Apply threshold to a signal 
    
    Args:
        sig: numpy.array of the signal to be thresholded
        th: threshold value over one
        
    Returns:
        sig: thresholded signal
    """
    sig = sig / np.max(sig)
    sig[sig < th] = 0
    sig[sig >= th] = 1
    return sig

def freq2MIDI(freq):
    """Converts frequency values array to midi values array

    Args:
        freq: numpy.array containing the frequencies

    Returns:
        midi: numpy.array containing the midi (non quantized) values.

    """
    freq = np.array(freq)
    midi = np.log2(freq/440.0) * 12 + 69
    return midi

def apply_masks(array, *args):
    """Apply masks to array
    
    Args:
        array: numpy.array of the signal to be masked
        *args: list of the masks to be applied
        
    Returns:
        array: masked array
    """
    for arg in args:
        array = np.multiply(array, arg)
    return array

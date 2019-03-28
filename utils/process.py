import numpy as np
from utils.mpd import *
from utils.mptc import *
from utils.traj_seg import *
import matplotlib.pyplot as plt

def process_audio(audio):

    audio_multi_pitch = mpd(audio)

    freq_arr = mptc(audio_multi_pitch)

    freq_arr_masked = trajectory_segmentation(audio, freq_arr)

    return freq_arr_masked

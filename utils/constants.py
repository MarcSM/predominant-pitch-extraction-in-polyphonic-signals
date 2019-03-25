import numpy as np
import os

eps = np.finfo(float).eps

SAMPLE_RATE = 44100  # Sample rate
ANALYZE_SOUND_FRAME_SIZE = 2048  # Surce sound analysis frame sizes
HOP_SIZE = 256  # Parameter used by the "FrameGenerator" and "FFT" functions

os.chdir('..')
ROOT_PATH = os.getcwd()
os.chdir('project_notebooks')

DATASET_PATH = os.path.join(ROOT_PATH, 'data', 'adc2004_full_set')

WAV_FOLDER = os.path.join(DATASET_PATH, "wav")
OUTPUT_PLOT_FOLDER = os.path.join(DATASET_PATH, "plots")
REF_CSV_FOLDER = os.path.join(DATASET_PATH, "ref_csv")
EXT_CSV_FOLDER = os.path.join(DATASET_PATH, "ext_csv")
ERROR_CSV_FILE = os.path.join(DATASET_PATH, "error.csv")

if not os.path.isdir(OUTPUT_PLOT_FOLDER): os.makedirs(OUTPUT_PLOT_FOLDER)
if not os.path.isdir(REF_CSV_FOLDER): os.makedirs(REF_CSV_FOLDER)
if not os.path.isdir(EXT_CSV_FOLDER): os.makedirs(EXT_CSV_FOLDER)

#default autocorrelation parameters
MIN_F0 = 100
MAX_F0 = 1000

#default value for octave error correction
TOL_PERCENT = 1

#default value for energy mask computation
ENERGY_THRESHOLD = 0.1

#default threshold for frequency diff mask
MIDI_TH = 0.2

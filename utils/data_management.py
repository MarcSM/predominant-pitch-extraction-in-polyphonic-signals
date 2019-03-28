from utils.constants import *
import os
import numpy as np
import essentia.standard as estd
import pandas as pd
import matplotlib.pyplot as plt

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

    if not os.path.exists(os.path.join(EXT_CSV_FOLDER,filename + "EXT.txt")): open(os.path.join(EXT_CSV_FOLDER,filename + "EXT.txt"),"w+")
    with open(os.path.join(EXT_CSV_FOLDER,filename + "EXT.txt"),'w') as txtfile:
        for c1,c2 in zip(ms,pitch):
            
            txtfile.write("{:.3f}".format(c1)+"     " +
                          "{:.3f}".format(c2) + "\n")

def calculate_average_tsv(filepath):
    """Computes and appends the average values per columns in a tsv file
    
    Args:
        filepath: path to the file to be computed the average from
        
    """

    with open(ERROR_CSV_FILE,'r') as tsvfile:
        df = pd.read_csv(tsvfile, sep='\t', header = None,index_col = 0)
        
    del df.index.name
    df.columns = np.arange(len(df.columns))
    average = []
    for col in df:
        tmp = df[col].tolist()
        average.append(sum(tmp)/len(tmp))
    df2 = df.from_dict({"Average":average}, orient="index")
    df = df.append(df2)

    with open(ERROR_CSV_FILE,'w') as tsvfile:
        df.to_csv(tsvfile, header = False, sep='\t')

def calculate_difference_with_reference(extracted,reference):
	"""Computes and appends the average values per columns in a tsv file

	Args:
		filepath: path to the file to be computed the average from

	"""
	with open(extracted,'r') as tsvfile:
		extracted_df = pd.read_csv(tsvfile, sep='\t', header = None,index_col = 0)

	with open(reference,'r') as tsvfile:
		reference_df = pd.read_csv(tsvfile, sep='\t', header = None,index_col = 0)

	extracted_df = extracted_df.sub(reference_df)
	del extracted_df.index.name
	extracted_df.columns = ['evalOption1','evalOption2','Average']

	print(extracted_df)

	if os.path.exists(ERROR_COMP_CSV_FILE): os.remove(ERROR_COMP_CSV_FILE)
	with open(ERROR_COMP_CSV_FILE, 'w') as tsvfile:
		extracted_df.to_csv(tsvfile, sep='\t')

def plot_comparison(filename):
    """Computes and appends the average values per columns in a tsv file

	Args:
		filepath: path to the file to be computed the average from

    """
    
    essentia_folder = os.path.join(DATASET_PATH,"ess_ext_csv")
    our_folder = os.path.join(DATASET_PATH,"our_ext_csv")
    if not os.path.exists(essentia_folder): raise ValueError("")
    if not os.path.exists(our_folder): raise ValueError("")

    essentia_file = os.path.join(essentia_folder,filename + "EXT.txt")
    our_file = os.path.join(our_folder,filename + "EXT.txt")
    ref_file = os.path.join(REF_CSV_FOLDER,filename + "REF.txt")

    with open(essentia_file, 'r') as f:
        essentia_data = []
        for row in f:
            essentia_data.append(float(row.split('     ')[1].split('\n')[0]))

    with open(our_file, 'r') as f:
        our_data = []
        for row in f:
            our_data.append(float(row.split('     ')[1].split('\n')[0]))

    with open(ref_file, 'r') as f:
        ref_data = []
        for row in f:
            ref_data.append(float(row.split('     ')[1].split('\n')[0]))
        ref_data.append(0)

    ms = np.round(np.arange(len(ref_data))*HOP_SIZE/SAMPLE_RATE,decimals=3)
    #print(len(our_data), len(essentia_data), len(ref_data))

    f,axes = plt.subplots(3,1,figsize=(15,15))

    axes[0].plot(ms,our_data)
    axes[0].set_title("Extracted Pitch")
    axes[0].grid(b = True, axis = 'both', color = 'k', linestyle = '-', linewidth = 0.3)
    axes[0].set_ylabel('Freqs in Hz')

    axes[1].plot(ms,essentia_data)
    axes[1].set_title("Essentia Pitch")
    axes[1].grid(b = True, axis = 'both', color = 'k', linestyle = '-', linewidth = 0.3)
    axes[1].set_ylabel('Freqs in Hz')

    axes[2].plot(ms,ref_data)
    axes[2].set_title("Reference Pitch")
    axes[2].grid(b = True, axis = 'both', color = 'k', linestyle = '-', linewidth = 0.3)
    axes[2].set_ylabel('Freqs in Hz')
    axes[2].set_xlabel('s')
    
    plot_file = os.path.join(OUTPUT_PLOT_FOLDER, filename+"_results.png")
    plt.savefig(plot_file)
    plt.show()
    #plt.close()
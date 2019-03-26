import numpy as np
import os
from utils.constants import *

def compute_error(filename):
    """Calls evalOption1 and evalOption2 and stores the values in a txt file
    
    Args:
        extracted: name of trhe file to extract without extension
        reference: sample rate

    """

    reference = os.path.join(REF_CSV_FOLDER, filename + "REF.txt")
    extracted = os.path.join(EXT_CSV_FOLDER, filename + "EXT.txt")

    totalMatch1, _, _ = evalOption1(extracted, reference)
    totalMatch2, _, _ = evalOption2(extracted, reference)

    avg = (totalMatch1 + totalMatch2)/2

    with open(ERROR_CSV_FILE, 'a') as txtfile:
        txtfile.write(filename + '\t' + str(totalMatch1) +
                      '\t' + str(totalMatch2) + '\t' + str(avg) + '\n')

def evalOption1(extracted, reference):
    """algorithm for the evaluation of melody extractors after option 1
    
    Args:
        extracted: string with path/filename of the extracted melody
        reference: string with path/filename of the reference melody

    Both files are assumed to be ASCII files containing data at the same frame rate.
    Unpitched frames are coded as 0Hz pitch.
    The algorithm assumes that the pitch information in Hz for each frame is stored in the last column of the files.

    Returns:
        pitchMatch: Concordance measure for the pitched frames (in reference) only
        unpitchMatch: Concordance measure for the unpitched frames (in reference) only
        totalMatch: Combined concordance measure
    """

    mel1 = []
    with open(extracted, 'r') as f:
        for line in f:
            tmp = line.split('\n')[0].split('     ')
            mel1.append(tmp)

    mel1 = np.array(mel1)
    frames1, cols = mel1.shape
    mel1 = mel1[:,cols-1]

    mel2 = []
    with open(reference, 'r') as f:
        for line in f:
            tmp = line.split('\n')[0].split('     ')
            mel2.append(tmp)

    mel2 = np.array(mel2)
    frames2, cols = mel2.shape
    mel2 = mel2[:,cols-1]

    if frames1<frames2:
        mel1.append(np.zeros(frames2-frames1))
    
    if frames1>frames2:
        mel1 = mel1[:frames2]

    unpitched = [1 for item in mel2 if float(item)==0.0] 
    nopitchdet = [1 for item1,item2 in zip(mel1,mel2) if (float(item1)==0.0) and (float(item2)==0.0)]
    
    if len(nopitchdet) == len(unpitched): unpitchMatch = 100
    elif len(unpitched) == 0: unpitchMatch = 0
    else: unpitchMatch = 100*len(nopitchdet)/len(unpitched)

    for item,idx in zip(mel1,range(frames2)):
        if float(item)!=0.0:
            mel1[idx] = 1200*(np.log2(float(item)/13.75)-0.25)
        else:
            mel1[idx] = float(item)
    
    for item,idx in zip(mel2,range(frames2)):
        if float(item)!=0.0:
            mel2[idx] = 1200*(np.log2(float(item)/13.75)-0.25)
        else:
            mel1[idx] = float(item)
    
    errCent = np.absolute([float(item1)-float(item2) for item1,item2 in zip(mel1,mel2)])

    errCent = [min(100,float(item)) for item in errCent]
    totalMatch = 100 - sum(errCent)/len(errCent)
    errCent = [float(item) for item in errCent if float(item)!=0.0]
    pitchMatch = 100 - sum(errCent)/len(errCent)

    return totalMatch, pitchMatch, unpitchMatch

def evalOption2(extracted, reference):
    """algorithm for the evaluation of melody extractors after option 2
    
    Args:
        extracted: string with path/filename of the extracted melody
        reference: string with path/filename of the reference melody

    Both files are assumed to be ASCII files containing data at the same frame rate. 
    Unpitched frames are coded as 0Hz pitch.
    The algortihm assumes that the pitch information in Hz for each frame is stored in the last column of the files.

    Returns:
        pitchMatch: Concordance measure for the pitched frames (in reference) only
        unpitchMatch: Concordance measure for the unpitched frames (in reference) only
        totalMatch: Combined concordance measure
    """
    mel1 = []
    with open(extracted, 'r') as f:
        for line in f:
            tmp = line.split('\n')[0].split('     ')
            mel1.append(tmp)

    mel1 = np.array(mel1)
    frames1, cols = mel1.shape
    mel1 = mel1[:,cols-1]

    mel2 = []
    with open(reference, 'r') as f:
        for line in f:
            tmp = line.split('\n')[0].split('     ')
            mel2.append(tmp)

    mel2 = np.array(mel2)
    frames2, cols = mel2.shape
    mel2 = mel2[:,cols-1]

    if frames1<frames2:
        mel1.append(np.zeros(frames2-frames1))
    
    if frames1>frames2:
        mel1 = mel1[:frames2]

    unpitched = [1 for item in mel2 if float(item)==0.0] 
    nopitchdet = [1 for item1,item2 in zip(mel1,mel2) if (float(item1)==0.0) and (float(item2)==0.0)]

    if len(nopitchdet) == len(unpitched): unpitchMatch = 100
    elif len(unpitched) == 0: unpitchMatch = 0
    else: unpitchMatch = 100*len(nopitchdet)/len(unpitched)

    for item,idx in zip(mel1,range(frames2)):
        if float(item)!=0.0:
            item = 1200*(np.log2(float(item)/13.75)-0.25)
            mel1[idx] = 100 + np.mod(item,1200)
        else:
            mel1[idx] = float(item)
    
    for item,idx in zip(mel2,range(frames2)):
        if float(item)!=0.0:
            item = 1200*(np.log2(float(item)/13.75)-0.25)
            mel2[idx] = 100 + np.mod(item,1200)
        else:
            mel1[idx] = float(item)

    errCent = np.absolute([float(item1)-float(item2) for item1,item2 in zip(mel1,mel2)])

    for itemmel1, itemmel2, itemerr, idx in zip(mel1,mel2,errCent,range(frames2)):
        if (float(itemerr)>600) and (float(itemmel1)!=0.0) and (float(itemmel2)!=0.0):
            errCent[idx] = 1200 - float(itemerr)

    errCent = [min(100,float(item)) for item in errCent]

    totalMatch = 100 - sum(errCent)/len(errCent)
    errCent = [float(item) for item in errCent if float(item)!=0.0]
    pitchMatch = 100 - sum(errCent)/len(errCent)

    return totalMatch, pitchMatch, unpitchMatch

import numpy as np
import matplotlib.pyplot as plt

def evalOption1(extracted, reference = ''):
    
    print('-------------------------------------')

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
            tmp = line.split('\n')[0].split('\t')
            mel2.append(tmp)

    mel2 = np.array(mel2)
    frames2, cols = mel2.shape
    mel2 = mel2[:,cols-1]

    if frames1<frames2:
        print(' Warning! Extracted melody is shorter than the reference!')
        print(' Zeros are appended.')
        mel1.append(np.zeros(frames2-frames1))
    
    if frames1>frames2:
        print(' Warning! Extracted melody is shorter than the reference!')
        print(' Zeros are appended.')
        mel1 = mel1[:frames2]

    unpitched = [1 for item in mel2 if float(item)==0.0] 
    nopitchdet = [1 for item1,item2 in zip(mel1,mel2) if (float(item1)==0.0) and (float(item2)==0.0)]
    unpitchMatch = 100*len(nopitchdet)/len(unpitched)
    print('Unpitched frame accordance: ',"{:.2f}".format(unpitchMatch),'%')

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

    print('Pitched frame accordance: ',"{:.2f}".format(pitchMatch),'%')
    print('TOTAL ACCORDANCE: ',"{:.2f}".format(totalMatch),'%')
    print('-------------------------------------')



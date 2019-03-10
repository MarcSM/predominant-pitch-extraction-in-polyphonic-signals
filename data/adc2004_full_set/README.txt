README.txt for adc2004_full_set.zip

ADC2004 Audio Melody Extraction Evaluation Data

This package contains the twenty short audio files plus ground-truth 
melody fundamental frequency transcripts for the Melody Extraction 
evaluation conducted as part of the 2004 ISMIR Audio Description 
Contests (ADC).  These data were prepared by Emilia Gomez, Beesuan Ong, 
and Sebastian Streich of the Universitat Pompeu Fabra in Barcelona, Spain, 
and is more fully described at:

http://ismir2004.ismir.net/melody_contest/results.html

Unfortunately, the link to the evaluation data on that page, pointing to 

http://www.iua.upf.es/mtg/ismir2004/contest/melodyContest/FullSet.zip

is not working at present, so we have built a new archive, consisting 
of the files we previously downloaded in this set, to provide interim 
access.

There are 20 audio files in Microsoft WAV format, all mono at 44.1 kHz 
sampling rate, with duration from 10 to 25 seconds.  For each file e.g. 
daisy1.wav, there is a corresponding transcription file daisy1REF.txt 
which consists of lines:

<time_in_sec>  <f_0_in_Hz>

The times increment in steps of 5.805 ms (256/44100), with one line 
for every window.  The manually-verified f_0 values report 0 for frames 
which are judged not to contain a foreground melody note, otherwise 
give the fundamental frequency of the foreground (melody) pitch to a 
nominal sub-1 Hz resolution.

Dan Ellis dpwe@ee.columbia.edu 2010-08-22

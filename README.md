# MIR Project

## Predominant pitch extraction in polyphonic signals
*Performance and accuracy evaluation of PredominantPitchMelodia and the ISMIR’s 2004 contest winner Rui Pedro Paiva*

### Abstract

Music in general is **polyphonic** (multiple pitches sounding at the same time) and there usually is a melodic line that stands above the rest of the sounds. In this paper, a study of **Rui Pedro Paiva’s** proposed structure for Predominant Pitch Extraction is compared against Essentia’s **PredominantPitchMelodia** and an implementation of the authors based on Paiva’s structural algorithm. These three algorithms have the same goal, which is to detect and isolate the main melodic line from the rest. In the end we conclude that the essentia algorithm is, by today's standards the best in terms of performance and accuracy and we propose some possible lines of further investigation for the work done in this paper.

### Description

This repository contains a docker-compose file to run a Jupyter server. To run the notebooks, you need to first install docker and run the Jupyter server available in the docker image.

## Install docker

### Windows
https://docs.docker.com/docker-for-windows/install/

### Mac
https://docs.docker.com/docker-for-mac/install/

### Ubuntu
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce

## Running the Jupyter server 
In a terminal/console window, change to this directory

On MacOS or Windows, run:

    docker-compose up

On Linux, run the following (this command ensures that any files you create are owned by your own user):

    JUPYTER_USER_ID=$(id -u) docker-compose up

The first time you run this command it will download the required docker images (about 2GB in size). If you have previously downloaded the images and would like to update them with the last version, run:

    docker-compose pull

Then accesss http://localhost:8888 with your browser and when asked for a
password use the default password ***mir***

Then, you can access the notebooks from the browser and run them.

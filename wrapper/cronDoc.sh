#!/bin/bash
#Cron job to run fMRIPrep through docker wrapper on Mac OSX Sierra
echo 'Running fMRIPrep on Subject'
source /path/to/username/.bash_profile
fmriprep-docker-cron /path/to/username/ProjectDir/BIDSdir /path/to/username/ProjectDir/BIDSdir/derivatives participant --participant-label <participant-label> --fs-license-file /path/to/freesurfer.txt

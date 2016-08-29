#!/bin/bash

./pyburst_excesspower_gnome_gauss --verbose --gps-start-time 0 --max-frequency 250 --pad-data 4 --gps-end-time 1 --min-frequency 0 --psd-segment-stride 30 --channel-name H1:FAKE-STRAIN --sample-rate 500 --channels 1023 --psd-segment-length 60 --psd-estimation median-mean --tile-fap 1e-5

import biobss
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp



def load_data(dir):
    """
    Load data from the data folder
    """
    # Load data
    data = []
    order = []
    for file in os.listdir(dir):
        if file.endswith(".csv"):
            print(os.path.join(dir, file))
            df = pd.read_csv(os.path.join(dir, file),on_bad_lines='skip')
            if not df.empty:
                order.append(int(file[:-4]))
                data.append(df['DATA'])
    return data, order


def preprocess(data, window_size = 600, fs = 24):
    """
    Preprocess data using BioBSS
    Returns: HRV measures for each specified window
    """
    # Preprocess data

    new_data = []
    
    for i in range(len(data)):
        windowed_data = []
        sig = data[i]

        sig = biobss.preprocess.filter_signal(sig,sampling_rate=fs,signal_type='PPG', method='bandpass')
        sig = biobss.preprocess.normalize_signal(sig)
        temp = biobss.preprocess.signal_segment(sig,window_size=window_size,step_size=window_size/2)
        for j in range(len(temp)):
            sigs = temp[j]
            info=biobss.preprocess.peak_detection(sigs,fs,'peakdet',delta=0.01)

            locs_peaks=info['Peak_locs']
            peaks=sig[locs_peaks]
            locs_onsets=info['Trough_locs']
            onsets=sig[locs_onsets] 

            info=biobss.ppgtools.peak_control(sig=sigs, peaks_locs=locs_peaks, troughs_locs=locs_onsets)

            locs_peaks=info['Peak_locs']
            peaks=sig[locs_peaks]
            locs_onsets=info['Trough_locs']
            onsets=sig[locs_onsets]

            temp[j] = biobss.hrvtools.get_hrv_features(sampling_rate=fs, signal_length=len(sigs)/fs, input_type='peaks',peaks_locs=locs_peaks)
        new_data.append(temp)

    return new_data

try:
    Group1, Group1_order = load_data("/mnt/ArtHeart/Data/Group 1")
    Group2, Group2_order = load_data("/mnt/ArtHeart/Data/Group 2")
    Group3, Group3_order = load_data("/mnt/ArtHeart/Data/Group 3")
except:
    try:
        Group1, Group1_order = load_data("Data/Group 1")
        Group2, Group2_order = load_data("Data/Group 2")
        Group3, Group3_order = load_data("Data/Group 3")
    except:
        Group1, Group1_order = load_data("W:\PhD\ArtHeart\Data\Group 1")
        Group2, Group2_order = load_data("W:\PhD\ArtHeart\Data\Group 2")
        Group3, Group3_order = load_data("W:\PhD\ArtHeart\Data\Group 3")


Group1 = preprocess(Group1)
Group2 = preprocess(Group2)
Group3 = preprocess(Group3)
"""
@author: elamr
https://openneuro.org/datasets/ds004504/versions/1.0.8/download
Data Citation: Andreas Miltiadous, Katerina D. Tzimourta, Theodora Afrantou, Panagiotis Ioannidis, Nikolaos Grigoriadis, Dimitrios G. Tsalikakis, Pantelis Angelidis, Markos G. Tsipouras, Evripidis Glavas, Nikolaos Giannakeas, and Alexandros T. Tzallas (2024). A dataset of EEG recordings from: Alzheimer's disease, Frontotemporal dementia and Healthy subjects. OpenNeuro. [Dataset] doi: doi:10.18112/openneuro.ds004504.v1.0.8
""" 
#LSM model training utils
import os
import tensorflow as tf
import keras
import pandas as pd
import mne
import numpy as np
import matplotlib.pyplot as plt

labels = pd.read_csv('./ModelTraining/EEG/data/ds004504-download/participants.tsv', sep='\t')

print(labels.head())

labels = labels[['participant_id', 'Group']]
print(labels.head())

eeg_files = []
data_path = './ModelTraining/EEG/data/ds004504-download/sub-'

for i in range(1, 88):
    sub_id = str(i).zfill(3)
    eeg_path = data_path + sub_id + '/eeg/'
    if os.path.exists(eeg_path):
        for file in os.listdir(eeg_path):
            if file.endswith('.set'):
                eeg_files.append((eeg_path + file, sub_id))
                print(f"Found EEG file: {eeg_path + file} for subject {sub_id}")

    else:
        print(f"Path does not exist: {eeg_path}")
print(f"Total EEG files found: {len(eeg_files)}")

eeg_data = []
eeg_labels = []
for file, sub_id in eeg_files:
    raw = mne.io.read_raw_eeglab(file, preload=True, verbose=False)
    raw.resample(128, npad="auto") 
    raw.filter(0.5, 40, fir_design='firwin') 
    data = raw.get_data() 
    eeg_data.append(data)
    group = labels.loc[labels['participant_id'] == f'sub-{sub_id}', 'Group'].values[0]
    eeg_labels.append(group)
    print(f"Processed EEG file: {file} for subject {sub_id} with group {group}")

label_mapping = {'A': 0, 'C': 1, 'F': 2}
eeg_labels = [label_mapping[label] for label in eeg_labels]
print(f"Total EEG data samples: {len(eeg_data)}")

max_length = max(data.shape[1] for data in eeg_data)

for i in range(len(eeg_data)):
    data = eeg_data[i]
    if data.shape[1] < max_length:
        pad_width = max_length - data.shape[1]
        eeg_data[i] = np.pad(data, ((0, 0), (0, pad_width)), mode='constant', constant_values=0)

eeg_data = np.array(eeg_data)
eeg_labels = np.array(eeg_labels)
eeg_labels = keras.utils.to_categorical(eeg_labels, num_classes=3)

print(f"EEG data shape: {eeg_data.shape}, EEG labels shape: {eeg_labels.shape}")
np.save('./ModelTraining/EEG/data/eeg_data.npy', eeg_data)

plt.plot(eeg_data[3][:, :np.count_nonzero(eeg_data[0][0])].T)
plt.title('Sample EEG Data (Non-Padded Portion)')
plt.show()




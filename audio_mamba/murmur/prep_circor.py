"""
Author: Adrian Florea
Date: 06/10/2024
"""

import os
import csv

import json
import re

import soundfile as sf
import librosa
import random

# Function to create JSON entries for each data entry
def create_json_entry(file_path, label):
    return {
        "wav": file_path,
        "labels": label
    }



def convert_wav_to_flac(wav_file_path, flac_file_path, wav_file_name):
    # Load the .wav file

    data, samplerate = sf.read(wav_file_path)


    # Resample the data to 16000 Hz (if it's not already at that sample rate)
    if samplerate != 16000:
        data_resampled = librosa.resample(data.T, samplerate, 16000).T

    # Write the resampled data to FLAC format
   # print(flac_file_path)

    save_path = os.path.join(flac_file_path,wav_file_name[:len(wav_file_name)-4] + '.flac')
    print(save_path)
    sf.write(save_path, data_resampled, 16000, format='flac')

    

def resample_each(file_path, lookup, save_path, read_dir, train_data):

    with open(file_path, 'r') as file:

        for line in file: 
            # Change later so that it searches for the type of murmur
            input = line.strip()
            if input.startswith('#'):
                break

            words = input.split()
            if len(words) == 3: #ID, number of locs, fs
                id = words[0]
                nlocs = words[1]
                fs = words[2]
                murmur_type = lookup[id]


                if id in train_data:
                    out_path = os.path.join(save_path,'train')
                else: 
                    out_path = os.path.join(save_path,'eval')


            
            elif len(words) == 4 : # PV 49989_PV.hea 49989_PV.wav 49989_PV.tsv
                wav_file = words[2]
                read_file = os.path.join(read_dir,wav_file)

                convert_wav_to_flac(wav_file_path=read_file, flac_file_path=out_path, wav_file_name=wav_file)



# Function to extract data from the CSV file
def extract_data(csv_file_path):
    unique_values = set()  # Set to store unique values
    subj_murmur = {}
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Check if the required columns exist
            if 'Murmur' not in reader.fieldnames or 'Systolic murmur timing' not in reader.fieldnames:
                print("Required columns not found in the CSV file.")
                return
            
            # Loop through each row in the CSV file
            for row in reader:
                subject = row['Patient ID']
                murmur_data = row['Murmur'].lower()
                systolic_timing_data = row['Systolic murmur timing'].lower()
                
                if systolic_timing_data != 'nan':
                    # Concatenate data with a dash
                    concatenated_data = murmur_data + '-' + systolic_timing_data
                else : 
                    concatenated_data = murmur_data

                subj_murmur[subject] = concatenated_data
                unique_values.add(concatenated_data)
            
    except IOError:
        print("File not found")

    return list(unique_values), subj_murmur


# Get all label types 
label_dir = '/home/icsl/Documents/adrian/classification/the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data.csv'
unique_labels, subj_murmur_lookup = extract_data(label_dir)

murmur_lists = {}
for subject_id, murmur_type in subj_murmur_lookup.items():
    if murmur_type not in murmur_lists:
        murmur_lists[murmur_type] = []
    murmur_lists[murmur_type].append(subject_id)

train_data = []
test_data = []

for murmur_type, subject_list in murmur_lists.items():
    random.shuffle(subject_list)
    split_point = int(len(subject_list) * 0.8)
    train_data.extend(subject_list[:split_point])
    test_data.extend(subject_list[split_point:])


# Make jason files for each 

read_dir = '/home/icsl/Documents/adrian/classification/the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data'

# make csv for label types 
csv_output = '/home/icsl/Documents/adrian/classification/pre_trained_mamba/class_labels_indices.csv'

with open(csv_output , 'w') as csvfile:
    csv_writer = csv.writer(csvfile)

    csv_writer.writerow(['index', 'mid','display_name'])

    for index , murmur_type in enumerate(unique_labels, start =1):
        csv_writer.writerow([index, murmur_type, murmur_type])

flac_file_path = '/home/icsl/Documents/adrian/classification/pre_trained_mamba/data'

# Loop through each file in the folder
for filename in os.listdir(read_dir):
    if filename.endswith('txt'):
        #only open .txt files 
        file_path = os.path.join(read_dir,filename)

        resample_each(file_path=file_path, lookup = subj_murmur_lookup, save_path=flac_file_path, read_dir= read_dir, train_data = train_data)


train_json_entries = []
for subject_id in train_data:
    file_path = os.path.join(flac_file_path,'/train',f"{subject_id}.flac")
    train_json_entries.append(create_json_entry(file_path=file_path, label=subj_murmur_lookup[subject_id]))

# Collect JSON entries for test data
test_json_entries = []
for subject_id in test_data:
    file_path = os.path.join(flac_file_path,'/test', f"{subject_id}.flac")
    test_json_entries.append(create_json_entry(file_path=file_path, label=subj_murmur_lookup[subject_id]))

train_json_output_path = '/home/icsl/Documents/adrian/classification/pre_trained_mamba/data/train/circor_train.json'
test_json_output_path = '/home/icsl/Documents/adrian/classification/pre_trained_mamba/data/eval/circor_test.json'

# Write the training data JSON entries to a file
with open(train_json_output_path, 'w') as train_json_file:
    json.dump(train_json_entries, train_json_file, indent=4)

# Write the test data JSON entries to a file
with open(test_json_output_path, 'w') as test_json_file:
    json.dump(test_json_entries, test_json_file, indent=4)
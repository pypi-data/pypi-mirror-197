# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 07:51:17 2023

@author: dreji18

this script is created from https://github.com/CorentinJ/Real-Time-Voice-Cloning
"""

import argparse
import os
from pathlib import Path

import librosa
import numpy as np
import pandas as pd
import soundfile as sf
import torch
import sounddevice as sd
from playsound import playsound
#from git import Repo
#import shutil

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

from encoder import inference as encoder
from encoder.params_model import model_embedding_size as speaker_embedding_size
from synthesizer.inference import Synthesizer
from utils.argutils import print_args
from utils.default_models import ensure_default_models
from vocoder import inference as vocoder

from scipy.io import wavfile
import noisereduce as nr

#%%
# allocating cuda infra if available
if torch.cuda.is_available():
    device_id = torch.cuda.current_device()
    gpu_properties = torch.cuda.get_device_properties(device_id)
    ## Print some environment information (for debugging purposes)
    print("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
        "%.1fGb total memory.\n" %
        (torch.cuda.device_count(),
        device_id,
        gpu_properties.name,
        gpu_properties.major,
        gpu_properties.minor,
        gpu_properties.total_memory / 1e9))
else:
    print("Using CPU for inference.\n")

#%%
# loading all the model artefacts
def load_model(model_type):
    if model_type == "indian":
        repo_name = "Indian-voice-cloning"
    else:
        repo_name = "default"
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-e", "--enc_model_fpath", type=Path,
                        default="saved_models/"+repo_name+"/encoder.pt",
                        help="Path to a saved encoder")
    parser.add_argument("-s", "--syn_model_fpath", type=Path,
                        default="saved_models/"+repo_name+"/synthesizer.pt",
                        help="Path to a saved synthesizer")
    parser.add_argument("-v", "--voc_model_fpath", type=Path,
                        default="saved_models/"+repo_name+"/vocoder.pt",
                        help="Path to a saved vocoder")
    args = parser.parse_args()
    
    if model_type == "indian": 
        # Check if the Indian-voice-cloning folder already exists
        if not os.path.exists(os.path.join(path, "saved_models", "Indian-voice-cloning")):
            os.chdir(path + "\\saved_models")
            # Install Git LFS
            os.system("git lfs install")
    
            # Clone the repository
            os.system("git clone https://huggingface.co/Vinotha/Indian-voice-cloning")
            os.chdir(path)
        else:
            print("Indian-voice-cloning folder already exists. Skipping clone step.")
            
    else:
        ensure_default_models(Path("saved_models"))

    enc_model_fpath = os.path.join(path, "saved_models/"+repo_name+"/encoder.pt")
    syn_model_fpath = os.path.join(path, "saved_models/"+repo_name+"/synthesizer.pt")
    voc_model_fpath = os.path.join(path, "saved_models/"+repo_name+"/vocoder.pt")
    
    encoder.load_model(enc_model_fpath)
    synthesizer = Synthesizer(syn_model_fpath)
    vocoder.load_model(voc_model_fpath)
    
    return encoder, synthesizer, vocoder,  args

def speech_generator(speech_text, voice_type=None, gender=None, speaker_id=None, sound_path=None):
    
    encoder, synthesizer, vocoder, args = None, None, None, None # defining the variables before they are used
    if voice_type == "western" or voice_type is None:
        encoder, synthesizer, vocoder, args = load_model(model_type="default")
    elif voice_type == "indian":
        try:
            encoder, synthesizer, vocoder, args = load_model(model_type="indian")
        except FileNotFoundError as e:
            print("\n-------Error-----------")
            print("Error: Indian-voice-cloning failed to download. You may download models manually instead from this drive : ")
            print("https://drive.google.com/drive/folders/1KVqc0HZCtBNwQka7YQ60iRNieC8RPM2b?usp=sharing")
            print(f"\nSave the model in this folder: {os.path.join(path, 'saved_models', 'Indian-voice-cloning')}")
            return 
    
    if sound_path:
        in_fpath = Path(sound_path.replace("\"", "").replace("\'", ""))
        original_wav, sampling_rate = librosa.load(str(in_fpath))
        preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    else:
        speaker_library = pd.read_excel(path+"\\speakers\\speaker_library.xlsx")
        audio_file = speaker_library[(speaker_library['voice_type']==voice_type) & 
                 (speaker_library['gender']==gender) & 
                 (speaker_library['speaker_id']==speaker_id)]['speaker'].values[0]

        in_fpath = os.path.join(path, "speakers", voice_type, gender, audio_file)

        original_wav, sampling_rate = librosa.load(str(in_fpath))
        preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)

    embed = encoder.embed_utterance(preprocessed_wav)
    synthesizer = Synthesizer(args.syn_model_fpath)
    
    if not os.path.isfile(args.syn_model_fpath):
        print("\n-------Error-----------")
        print("Error: 'synthesizer.pt' file not found in the Indian-voice-cloning model directory.")
        print("You may download synthesizer.pt file manually from this drive : ")
        print("https://drive.google.com/drive/folders/1KVqc0HZCtBNwQka7YQ60iRNieC8RPM2b?usp=sharing")
        print(f"\nSave the model in this folder: {os.path.join(path, 'saved_models', 'Indian-voice-cloning')}")
        return

    texts = [speech_text]
    embeds = [embed]

    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]
    print("Created the mel spectrogram")

    vocoder.load_model(args.voc_model_fpath)
    generated_wav = vocoder.infer_waveform(spec)
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    generated_wav = encoder.preprocess_wav(generated_wav)

    return generated_wav

def play_sound(generated_wav):
    if type(generated_wav) == np.ndarray:
        try:
            sd.stop()
            sd.play(generated_wav, 16000)
        except sd.PortAudioError as e:
            print("\nCaught exception: %s" % repr(e))
            print("Continuing without audio playback. Suppress this message with the \"--no_sound\" flag.\n")
    else:
        try:
            playsound(generated_wav)
        except:
            print("\nSorry, File could not be played!")


def play_library_sound(voice_type, gender, speaker_id):
    # map the speaker id with filename
    speaker_library = pd.read_excel(path+"\\speakers\\speaker_library.xlsx")

    try:
        audio_file = speaker_library[(speaker_library['voice_type']==voice_type) & 
                 (speaker_library['gender']==gender) & 
                 (speaker_library['speaker_id']==speaker_id)]['speaker'].values[0]
        
        # constructing the speaker file path
        sound_file_path = os.path.join(path, "speakers", voice_type, gender, audio_file)
        
        # try to play the sound file
        try:
            play_sound(sound_file_path)
        except Exception as e:
            print(f"Error: {e}. Couldn't play the sound file {sound_file_path}.")
        
    except IndexError:
        print(f"Error: The speaker_id {speaker_id} doesn't exist for voice_type={voice_type} and gender={gender}.")
        
    except Exception as e:
        print(f"Error: {e}. Couldn't construct sound_file_path.")

def save_sound(generated_wav, filename=False, noise_reduction=False):
    
    # noise reduction function
    def noise_reduction(generated_wav, file_out):
        rate = 16000
        data = generated_wav
        snr = 2 # signal to noise ratio
        noise_clip = data/snr
        reduced_noise = nr.reduce_noise(y=data, sr=rate, y_noise = noise_clip, n_std_thresh_stationary=1.5,stationary=True)
        
        wavfile.write(rate, reduced_noise, file_out)
        
    # Save it on the disk    
    if filename:
        file_out = filename + ".wav"
    else:
        file_out = "voice_output" + ".wav"
    
    if noise_reduction==True:
        noise_reduction(generated_wav, file_out)
    else:
        sf.write(file_out, generated_wav.astype(np.float32), 16000)

#%%



















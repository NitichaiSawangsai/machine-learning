import sys
import os
import torch
from torch.autograd import Variable
sys.path.insert(0, 'waveglow/')
import numpy as np
import time
import argparse
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import hparams as hp
from model import Tacotron2
from layers import TacotronSTFT
from audio_processing import griffin_lim
from denoiser import Denoiser


def load_model():
    checkpoint_path = "outdir/checkpoint_XXX"  # Replace with the path to your Tacotron 2 checkpoint
    model = Tacotron2()
    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    _ = model.cuda().eval().half()
    return model


def generate_mel_spectrogram(model, text):
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--textlist", type=str,
                        help='File containing text for processing')
    parser.add_argument("--output_directory", type=str, default="./", help="Location to save audio")
    parser.add_argument("--checkpoint_path", type=str, help="Location of Tacotron2 checkpoin")
    
    with torch.no_grad():
      sequence = np.array(text_to_sequence(text, ['english_cleaners']))[None, :]
      sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()
      mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
  
    return mel_outputs_postnet, alignments


def save_spectrogram(spectrogram, output_dir, filename):
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(np.rot90(spectrogram), aspect='auto', interpolation='none')
    fig.colorbar(im, ax=ax)
    plt.xlabel('Frames')
    plt.ylabel('Channels')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{filename}.png'))
    plt.close()


def main():
    model = load_model()
    text = "Hello, how are you?"  # Replace with the desired text to generate
    mel_outputs_postnet, alignments = generate_mel_spectrogram(model, text)
    save_spectrogram(mel_outputs_postnet[0].data.cpu().numpy(), './', 'spectrogram')

if __name__ == "__main__":
    main()
import os
import argparse

import soundfile as sf
import librosa
import psola
import scipy

import numpy as np


# Set some basis parameters
frame_length = 1024
fmin = librosa.note_to_hz('C2')
fmax = librosa.note_to_hz('D4')


def load_audio(filepath):
    """
    Loads the audio file.
    """

    # audio, sr = librosa.load(str(filepath), sr=None, mono=False)
    audio, sr = sf.read(str(filepath))

    # Only mono-files are handled. If stereo files are supplied, only the first channel is used.
    if audio.ndim > 1:
        audio = audio[0, :]

    return audio, sr


def detect_gender(f0):
    """
    Detects utterance gender based on the base frequencies.
    Works based on the fact that an adult woman's average pitch range is from 165 to 255 Hz and a man's is 85 to 155 Hz.
    """

    return "female" if f0[~np.isnan(f0)].mean() > 160 else "male"


def shift_pitch(sig, sr, f0, gender, kernel_size=11):
    """
    Shifts signal pitch by one octave based on the gender.
    """

    if gender == "female":
        shifted_f0 = f0 / 2
    else:
        shifted_f0 = f0 * 2

    # Perform median filtering to additionally smooth the corrected pitch.
    smoothed_shifted_f0 = scipy.signal.medfilt(shifted_f0, kernel_size=kernel_size)
    # Remove the additional NaN values after median filtering.
    smoothed_shifted_f0[np.isnan(smoothed_shifted_f0)] = shifted_f0[np.isnan(smoothed_shifted_f0)]

    shifted_sig = psola.vocode(sig, sample_rate=int(sr), target_pitch=smoothed_shifted_f0, fmin=fmin, fmax=fmax)

    return shifted_sig


if __name__ == '__main__':
    # Parsing the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', default='output.mp3', help='output file relative path')
    parser.add_argument('-g', '--gender', default=None, choices=['male', 'female'], help='input file utterance gender - empty to detect gender automatically')
    parser.add_argument('input', help='input file rlative path')
    args = parser.parse_args()

    # Loading audio
    sig, sr = load_audio(args.input)

    # Pitch tracking using the PYIN algorithm.
    f0, _, _ = librosa.pyin(sig,
                            frame_length=frame_length,
                            sr=sr,
                            fmin=fmin,
                            fmax=fmax)

    # Pitch shifting
    gender = args.gender if args.gender else detect_gender(f0)
    shifted_audio = shift_pitch(sig, sr, f0, gender)

    # Writing the output file
    sf.write(args.output, shifted_audio, sr)

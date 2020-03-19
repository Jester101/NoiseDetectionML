from scipy.io import wavfile

import matplotlib.pyplot as plot
from pathlib import Path

from pydub import AudioSegment

import os
import sys

SOURCE = 'source'
TMP = 'tmp'
DATA = 'data'
SPECTROGRAM_DIR = 'Spectrogram'
PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent


def convert_file(file_name):
    file = AudioSegment.from_mp3(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, file_name)))
    save_path = os.path.join(PROJECT_DIR, '{0}/{1}'.format(SOURCE, TMP))
    new_file_name = file_name.replace('.mp3', '.wav')
    try:
        file.export(os.path.join(save_path, new_file_name), format='wav')
    except Exception as ex:
        raise ex
    else:
        return save_path, new_file_name


def check_file_extension(file_name):
    extension = str(file_name).split('.')[1]
    if extension == 'wav':
        return True
    return False


def draw_spectrogram(sample_rate, signal_data):
    plot.specgram(signal_data, Fs=sample_rate)
    plot.axis('off')
    plot.legend('off')
    plot.tight_layout(pad=0)
    return plot


def create_spectrogram(file_name):
    file = os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, file_name))
    need_cleaning = False
    try:
        if not check_file_extension(file_name):
            need_cleaning = True
            path, file_name = convert_file(file_name)
            file = os.path.join(path, file_name)
    except Exception as ex:
        print(ex)
        return False
    else:
        sample_rate, audio_data = wavfile.read(file)
        fig = draw_spectrogram(sample_rate, audio_data)
        fig.savefig(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, file_name.replace('.wav', '.png'))))
        if need_cleaning:
            os.remove(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, TMP, file_name)))
        return True


if __name__ == '__main__':
    print(sys.argv[1])
    print(PROJECT_DIR)
    create_spectrogram(sys.argv[1])
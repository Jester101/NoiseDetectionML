import matplotlib.pyplot as plot

from pydub import AudioSegment
import numpy as np
import librosa
import librosa.display as display

from .image_changing import (
    crop_image,
    convert_png_to_grayscale,
    create_bmp_from_grayscale
)

import os
import sys

from cfg_load.config import (
    SOURCE,
    PROJECT_DIR,
    TMP,
    DATA
)

my_dpi = 96


def convert_file(file):
    file_segment = AudioSegment.from_mp3(file)
    save_path = os.path.join(PROJECT_DIR, '{0}/{1}'.format(SOURCE, TMP))
    new_file_name = file.replace('.mp3', '.wav').split('/')[-1]
    try:
        file_segment.export(os.path.join(save_path, new_file_name), format='wav')
    except Exception as ex:
        raise ex
    else:
        return save_path, new_file_name


def check_file_extension(file_name):
    extension = str(file_name).split('.')[1]
    if extension == 'wav':
        return True
    return False


def draw_spectrogram(signal_data):
    fig = plot.figure(figsize=(signal_data.shape[1] / 100, signal_data.shape[0] / 100))
    plot.axis('off')
    fig.legend('off')
    fig.tight_layout(pad=0)
    display.specshow(librosa.amplitude_to_db(signal_data, ref=np.max), y_axis='log', x_axis='time')
    return fig


def create_spectrogram(file, save_dir=DATA, mode='clear'):
    need_cleaning = False
    file_name = file.split('/')[-1]
    try:
        if not check_file_extension(file):
            need_cleaning = True
            path, file_name = convert_file(file)
            file = os.path.join(path, file_name)
    except Exception as ex:
        print(ex)
        return False
    else:
        audio_data, sample_rate = librosa.load(file)
        D = np.abs(librosa.stft(audio_data, n_fft=1024, hop_length=256, win_length=1024))
        fig = draw_spectrogram(D)
        save_directory = os.path.join(PROJECT_DIR, '{0}/{1}'.format(SOURCE, save_dir))
        if mode == 'clear':
            spectrogram_path = os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, TMP,
                                                                              file_name.replace('.wav', '.png')))
            fig.savefig(spectrogram_path)
            picture_arr = crop_image(spectrogram_path)
            for picture in picture_arr:
                create_bmp_from_grayscale(convert_png_to_grayscale(picture), save_directory)
            os.remove(spectrogram_path)
        else:
            spectrogram_path = os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, save_dir,
                                                                              file_name.replace('.wav', '.png')))
            fig.savefig(spectrogram_path)
            crop_image(spectrogram_path)
            os.remove(spectrogram_path)
        if need_cleaning:
            os.remove(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, TMP, file_name)))
        return True


if __name__ == '__main__':
    print(sys.argv[1])
    print(PROJECT_DIR)
    create_spectrogram(sys.argv[1])
from SoundController.Spectrogram import create_spectrogram
from SoundController.SoundMixing import mix_files

from mutagen.mp3 import MP3

from shutil import copyfile, rmtree
from random import randint
import uuid
import os
import sys

from cfg_load.config import (
    SOURCE,
    PROJECT_DIR,
    DATA,
    SOUND,
    MASKS,
    CLEAR,
    DIRTY,
    MIX,
    IMAGES,
    NOISE,
    DATASET
)

DATA_DIR = os.path.join(os.path.join(PROJECT_DIR, '{0}/{1}'.format(SOURCE, DATA)))
VOCAL_DATA_DIR = os.path.join(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, SOUND)))
NOISE_DATA_DIR = os.path.join(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, NOISE)))
MIX_DATA_DIR = os.path.join(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, MIX)))
CLEAR_DATA_DIR = os.path.join(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, CLEAR)))
DIRTY_DATA_DIR = os.path.join(os.path.join(PROJECT_DIR, '{0}/{1}/{2}'.format(SOURCE, DATA, DIRTY)))
DATABASE_DATA_DIR = os.path.join(os.path.join(PROJECT_DIR, '{0}/{1}'.format(SOURCE, DATASET)))

GLOBAL_DICT = dict()


def create_vocal_mask():
    for file in os.listdir(VOCAL_DATA_DIR):
        if file.endswith('.mp3'):
            create_spectrogram(os.path.join(VOCAL_DATA_DIR, file), DATA + '/' + CLEAR)


def create_spectrograms():
    for file in os.listdir(MIX_DATA_DIR):
        if file.endswith('.mp3'):
            create_spectrogram(os.path.join(MIX_DATA_DIR, file), DATA + '/' + DIRTY, mode='dirty')


def init_filenames_for_mixing():
    vocals = list()
    noises = list()
    for file in os.listdir(VOCAL_DATA_DIR):
        if file.endswith('.mp3'):
            vocals.append(file)
    for file in os.listdir(NOISE_DATA_DIR):
        if file.endswith('.mp3'):
            noises.append(file)
    return vocals, len(vocals), noises, len(noises)


def get_mp3_file_length(file):
    audio_file = MP3(file)
    return int(audio_file.info.length)


def random_file_mixing(file1, file2):
    print(file1)
    print(file2)
    file1_length = get_mp3_file_length(file1)
    file2_length = get_mp3_file_length(file2)
    mix_filename = '{0}_{1}'.format(file1.split('/')[-1].replace('.mp3', ''), file2.split('/')[-1])
    if file1_length > file2_length:
        mix_files(file1, file2, export_file_dir=MIX_DATA_DIR, export_file_name=mix_filename,
                  offset=randint(0, file1_length - file2_length - 1))
    else:
        mix_files(file1, file2, export_file_dir=MIX_DATA_DIR, export_file_name=mix_filename)


def random_files_mixing(repeats=1):
    used_noises = list()
    vocals, vocals_length, noises, noises_length = init_filenames_for_mixing()
    for i in range(repeats):
        used_noises.clear()
        for file in vocals:
            noise_number = randint(0, noises_length-1)
            while file in GLOBAL_DICT.keys() and GLOBAL_DICT[file] == noise_number:
                noise_number = randint(0, noises_length-1)
            GLOBAL_DICT[file] = noise_number
            random_file_mixing(os.path.join(VOCAL_DATA_DIR, file), os.path.join(NOISE_DATA_DIR, noises[noise_number]))


def find_mask(filename):
    for file in os.listdir(CLEAR_DATA_DIR):
        if file.startswith(filename) and file.endswith('.bmp'):
            return os.path.join(CLEAR_DATA_DIR, file)


def connect_data_with_masks():
    count = 1
    for file in os.listdir(DIRTY_DATA_DIR):
        if file.endswith('.png'):
            clear_file = find_mask(file.split('_')[0])
            frame_name = str(uuid.uuid4())
            save_dir = os.path.join(DATABASE_DATA_DIR, frame_name)
            try:
                os.mkdir(os.path.join(DATABASE_DATA_DIR, frame_name))
                os.mkdir(os.path.join(DATABASE_DATA_DIR, frame_name, IMAGES))
                os.mkdir(os.path.join(DATABASE_DATA_DIR, frame_name, MASKS))
                copyfile(os.path.join(DIRTY_DATA_DIR, file), os.path.join(save_dir,
                                                                          IMAGES + '/' + frame_name + '.png'))
                copyfile(os.path.join(clear_file), os.path.join(save_dir, MASKS + '/' + frame_name + '.bmp'))
            except Exception as ex:
                print(ex)
                return
            count += 1


def clean_before_preparation():
    GLOBAL_DICT.clear()
    for file in os.listdir(MIX_DATA_DIR):
        os.remove(os.path.join(MIX_DATA_DIR, file))
    for file in os.listdir(CLEAR_DATA_DIR):
        os.remove(os.path.join(CLEAR_DATA_DIR, file))
    for file in os.listdir(DIRTY_DATA_DIR):
        os.remove(os.path.join(DIRTY_DATA_DIR, file))
    if os.path.exists(DATABASE_DATA_DIR):
        rmtree(DATABASE_DATA_DIR)
    os.mkdir(DATABASE_DATA_DIR)


def prepare_dataset(repeats=1):
    clean_before_preparation()
    random_files_mixing(repeats)
    create_vocal_mask()
    create_spectrograms()
    connect_data_with_masks()


if __name__ == '__main__':
    if len(sys.argv[1]):
        print(len(sys.argv))
        try:
            prepare_dataset(int(sys.argv[1]))
        except Exception as ex:
            print(ex)
    else:
        prepare_dataset()

from pydub import AudioSegment
from pydub.utils import which

import os
import sys

GLOBAL_PATH = os.path.dirname(os.path.abspath(__file__))
CUT_COMMAND = " ffmpeg -i {0}.mp3 -f segment -segment_time 10 -c copy {0}%01d.mp3"
DELETE_COMMAND = "rm -rf {0}"
AudioSegment.converter = which('ffmpeg')
GLOBAL_DIR = os.path.dirname(os.path.abspath(__file__))


def mixing(audio_segment_first, audio_segment_second, position=0):
    difference = audio_segment_second.max_dBFS - audio_segment_first.max_dBFS
    # print(difference)
    if difference > 0:
        audio_segment_second += difference * 2
        # audio_segment_second = audio_segment_second.apply_gain(-difference + audio_segment_second.dBFS)
        # print('new ', audio_segment_second.dBFS)
    return audio_segment_first.overlay(audio_segment_second, position=position * 1000)


def read_file(path_to_file):
    audio_segment = AudioSegment.from_file(path_to_file)
    return audio_segment


def save_mixing_file(mixing_audio_segment, filename):
    mixing_audio_segment.export(filename, format='mp3')
    # filename_without_format = filename.replace('.mp3', '')
    # os.system(CUT_COMMAND.format(filename_without_format))


def mix_files(path_to_file1, path_to_file2, export_file_dir='', export_file_name="out.mp3", offset=0):
    segment1 = read_file(path_to_file1)
    segment2 = read_file(path_to_file2)
    output_segment = mixing(segment1, segment2, offset)
    # output_segment = output_segment.apply_gain(-20 - output_segment.dBFS)
    if export_file_name:
        save_mixing_file(output_segment, export_file_dir + '/' + export_file_name)
    else:
        save_mixing_file(output_segment, export_file_name)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Необходимо указать два файла")
        sys.exit()
    first_file_name = sys.argv[1]
    second_file_name = sys.argv[2]
    mix_files(
        GLOBAL_DIR + '/' + first_file_name,
        GLOBAL_DIR + '/' + second_file_name
    )
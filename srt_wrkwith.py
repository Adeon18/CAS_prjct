'''
This module is responsible for working with srt module and confortably
reading srt files and organising the data.
'''
import srt
from os import path

main_folder = path.dirname(__file__)
subtitles = path.join(main_folder, 'subtitles')


def read_data(subtitle_file: str) -> str:
    '''
    Read data from file and return a whole string of everything in file.
    '''
    with open(path.join(subtitles, subtitle_file)) as file:
        data = file.read()

    return data


def return_sub_list(data: str) -> list:
    '''
    Turn the string into a list of Subtitle objects and return that list.
    Remove all of the bad characters like newline ones.
    srt.parse takes only strings!!!
    '''
    subtitle_data = list(srt.parse(data))
    for subtitle in subtitle_data:
        subtitle.content = ' '.join(subtitle.content.split('\n'))
    
    return subtitle_data


if __name__ == '__main__':
    print(return_sub_list(read_data(path.join(subtitles, 'lil_prince_subtitles.srt'))))
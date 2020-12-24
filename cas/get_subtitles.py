'''
This module works with srt module.

Can read srt files, turn them into Subtitle objects and compress all of the
subtitles of a file to a list of Subtitle objects.

Functions:
    read_data
    return_sub_list
'''
import srt
from os import path


def read_data(subtitle_file: str) -> str:
    '''
    Read data from file and return a whole string of everything in file.

    Args:
        subtutle_file: Path to the file with subtitles.
    
    Returns:
        A string of the whole subtitle text read to pass to srt.parse later.
    '''
    with open(subtitle_file) as file:
        data = file.read()

    return data


def return_sub_list(data: str) -> list:
    '''
    Turn the string into a list of Subtitle objects and return that list.
    Remove all of the bad characters like newline ones.
    srt.parse takes only strings!!!

    Args:
        data: A string from read_data, which contains the whole subtitle file
        as it is.

    Returns:
        A list of subtitle objects of all the subtitles in data. Each subtitle
        object stores index, start, end, content, metadata of the subtitle.
    '''
    subtitle_data = list(srt.parse(data))
    for subtitle in subtitle_data:
        subtitle.content = ' '.join(subtitle.content.split('\n'))
    
    return subtitle_data


if __name__ == '__main__':
    pass
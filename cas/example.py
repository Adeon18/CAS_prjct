'''
This is the module responsible for launching most of the modules.

ATTENTION!!! This is just an example module and it will only work in case
you have the files named and put correctly.

Forlder
    lowercase_book_name
        subtitles
        book_text
        movie(optional)
        Also can find the movie and book similarities and create a file
        with them here
    this_module.py

This module asks you the name of the book, the citiation from it and if you
want to view it from the film(have to buy and download the film). Returns the
time that citiation is said in the film(if it is there) and optionally that
part of the film played with vlc video editor.
'''
import datetime
from os import path
from math import floor, ceil

import compare, launch_player, get_subtitles


def get_user_input():
    '''
    This is just a test function to get user input
    '''
    book_name = input('Enter a book name: ')
    citiation = input('Enter a citiation: ')
    movie_flag = input('Do you want to see citiation in a movie? ')

    return (book_name, citiation, movie_flag)

if __name__ =='__main__':
    try:
        book_name, citiation, flag = get_user_input()
        main_folder = path.dirname(__file__)
        movie_info = path.join(main_folder, book_name.lower().replace(' ', '_'))

        start, end = compare.check_for_presence(citiation,\
            get_subtitles.return_sub_list(get_subtitles.read_data(path.join(movie_info, 'subtitles.srt'))))

        try:
            print(f'{datetime.timedelta(seconds=start)} - {datetime.timedelta(seconds=end)}')
        except:
            print(start, end)

        if flag.lower() == 'yes':
            player = launch_player.Player(path.join(movie_info, 'movie.mp4'))
            # 17 is a cooldown for the little prince movie
            player.play_a_part(floor(start) + 17, 3*ceil(end - start))
    except:
        print('Write valid names or add missing files')




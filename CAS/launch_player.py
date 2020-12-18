'''
A module that can show media.

Contains a media player class that can show media in different ways,
including some parts.

Classes:
    Player: That media player class.
'''
import time, vlc
from os import path


class Player:
    '''
    A Class for creating and using a video player

    Methods
    -------
    play: Play a whole media
    return_duration: Returns media duration(in miliseconds)
    play_a_part: Plays a specific part of the media
    '''
    def __init__(self, source: str):
        self.source = source
        # Creating a vlc instance
        self.vlc_instance = vlc.Instance()
        # Creating a media player
        self.player = self.vlc_instance.media_player_new()
        # Creating a media(video)
        self.media = self.vlc_instance.media_new(self.source)
        # Setting up the player to play media
        self.player.set_media(self.media)

    def play(self):
        '''
        Play a whole media

        Uses return_duration to get the media duration and play the media for set time
        Duration is in miliseconds, so we divide it by 1000
        '''
        duration = self.return_duration()
        self.player.play()
        time.sleep(duration // 1000)
        # Close the player
        self.vlc_instance.vlm_stop_media(self.source)

    def return_duration(self):
        '''
        Returns media duration(in miliseconds)
        '''
        self.player.play()
        # Play media for one second, so we could get the time
        time.sleep(1)
        vid_duration = self.player.get_length()

        return vid_duration

    def play_a_part(self, start: int, duration: int):
        '''
        Plays a specific part of the media

        Args:
          start:
            Integer, must be in seconds
          duration:
            Integer, must be in seconds
        '''
        self.player.play()
        # set_time takes only miliseconds
        self.player.set_time(start*1000)
        # We play media from our set_time
        time.sleep(duration)
        # Close the player
        self.vlc_instance.vlm_stop_media(self.source)


if __name__ == '__main__':
    from os import path

    main_folder = path.dirname(__file__)
    movie_folder = path.join(main_folder, 'movies')
    # vid_player = Player("the_lil_prince.mp4")
    vid_player = Player(path.join(movie_folder, 'the_lil_prince.mp4'))

    vid_player.play()
    # print(vid_player.return_duration())
    # vid_player.play_a_part(10, 8)

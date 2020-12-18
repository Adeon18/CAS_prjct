'''
This module is responsible for sentence comparison.

Compares sentences from subtitles and a book and picks the ones that fall
under some coefficient of similarity.

Functions:
    read_text
    compare_subt_w_txt
    compare_2_sentences
    check_for_presence
'''
import datetime
import re
from os import path

import srt
import nltk

# This is for comparing
nltk.download('stopwords')


def read_text(path_to_file: str) -> list:
    '''
    Read the book and return a list of all sentences, formatted a bit.

    Args:
        path_to_file: Path to book text file within a folder
        (folder included already).
    
    Return:
        A list of formatted book sentences.
    '''
    with open(path_to_file) as file:
        data = file.read()

        data = re.split('[?.!]',data)
        for i, _ in enumerate(data):
            data[i] = ' '.join(data[i].split('\n'))
            data[i] = ''.join(data[i].split('”'))
            for _ in range(3):
                data[i] = ' '.join(data[i].split('  '))
    
    return data


def compare_subt_w_txt(subtitle_list: list, sentence_list: list,
                       filename: str) -> list:
    '''
    Compares the whole subtitle file with the whole book text file and writes
    the similar sentences in a file.

    Args:
        subtitle_list: List of all the subtitle objects.
        sentence_list: List of all the book .
        filename: The name of the file to write info to.

    Returns:
        Nothing, but writes data to a file. Sentences are written in 
        "sentence from movie - sentence from book" fashion.
    '''
    output_list = []
    for sentence in sentence_list:
        for subtitle in subtitle_list:
            # We don't double check
            if not [subtitle, sentence] in output_list:
                # similarity - float coeff
                similarity = compare_2_sentences(subtitle, sentence)
                # Define how similar should sentences be
                if similarity > 0.8:
                    output_list.append([subtitle, sentence])
                    break
        continue
    # Write the similarities
    with open('similarities.txt') as file:
        for i in output_list:
            file.write(f'{i[0].content} - {i[1]}\n')


def compare_2_sentences(sentence1: str, sentence2: str) -> float:
    '''
    Compares 2 sentences using ntlk module and returns.

    Args:
        sentence1: A subtitle object with all the attributes.
        sentence2: A sentence from a book text.

    Returns:
        Cosine - similarity coefficient, 0 <= cosine <= 1
    '''
    # Tokenization
    sentence_txt = nltk.tokenize.word_tokenize(sentence2)
    sentence_sub = nltk.tokenize.word_tokenize(sentence1.content)
    # Stopwords which will be deleted later
    sw = nltk.corpus.stopwords.words('english')
    # Lists for info storing
    lst1 = []
    lst2 = [] 
    # Remove stop words from the string
    sentence_sub_set = {w for w in sentence_sub if not w in sw}  
    sentence_txt_set = {w for w in sentence_txt if not w in sw} 
    # Form a set containing keywords of both strings  
    rvector = sentence_sub_set.union(sentence_txt_set)  
    # Put info in lists
    for w in rvector: 
        if w in sentence_sub_set: lst1.append(1) # create a vector
        else: lst1.append(0) 
        if w in sentence_txt_set: lst2.append(1) 
        else: lst2.append(0) 
    coef = 0
    
    # Cosine formula(Add similarities and divide by average sum)
    for i in range(len(rvector)): 
        coef += lst1[i]*lst2[i]
    try:  # Similariry calculation formula
        cosine = coef / float((sum(lst1)*sum(lst2))**0.5)
    except:
        # print('Error')
        cosine = 0.0

    return cosine


def check_for_presence(citiation: str, subtitle_list: list):
    '''
    Checks if a single book setence is present in the subtitles.

    Args:
        citiation: That book sentence.
        subtitle_list: List of subtitle objects.

    Returns:
        A tuple containing the start and the end of the subtitle in seconds if
        book sentence is in the subtitles.
        A tuple of 2 error messages otherwise.
    '''
    for subtitle in subtitle_list:
        similarity = compare_2_sentences(subtitle, citiation)
        if similarity > 0.8:
            return (subtitle.start.total_seconds(), subtitle.end.total_seconds())
    
    return ('No citiation present in a movie,', 'write a different one')


if __name__ == '__main__':
    from math import floor, ceil
    from get_subtitles import return_sub_list, read_data
    from launch_player import Player
    main_folder = path.dirname(__file__)
    movie_folder = path.join(main_folder, 'movies')
    subtitles = path.join(main_folder, 'subtitles')
    p = Player(path.join(movie_folder, 'the_lil_prince.mp4'))
    # print(read_text('lil_prince.txt'))
    # print(compare_subt_w_txt(return_sub_list(read_data('lil_prince_subtitles.srt')) ,read_text('lil_prince.txt')))
    strt, end = check_for_presence('But if you tame me, then we shall need each other', return_sub_list(read_data(path.join(subtitles, 'lil_prince_subtitles.srt'))))
    print(floor(strt), ceil(end - strt))
    p.play_a_part(floor(strt) + 17, 3*ceil(end - strt))
    # print(strt, end)

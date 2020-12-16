import re
import srt
from os import path
import nltk
import datetime
# from nltk.corpus import stopwords 
# from nltk.tokenize import word_tokenize
nltk.download('stopwords')

main_folder = path.dirname(__file__)
text_folder = path.join(main_folder, 'texts')
similarities_folder = path.join(main_folder, 'similarities')


def read_text(path_to_file: str) -> list:
    with open(path.join(text_folder, path_to_file)) as file:
        data = file.read()

        data = re.split('[?.!]',data)
        for i, _ in enumerate(data):
            data[i] = ' '.join(data[i].split('\n'))
            data[i] = ''.join(data[i].split('”'))
            for _ in range(3):
                data[i] = ' '.join(data[i].split('  '))
    
    return data


def compare_subt_w_txt(subtitle_list: list, sentence_list: list) -> list:
    '''
    Compares the whole subtitle file with the whole book text file and writes
    the similar sentences in a file.

    Sentences are written in "sentence from movie - sentence from book"
    fashion.
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
    with open(path.join(similarities_folder, 'lil_prince_simct.txt'), 'w') as file:
        for i in output_list:
            file.write(f'{i[0].content} - {i[1]}\n')


def compare_2_sentences(sentence1: str, sentence2: str) -> float:
    '''
    Compares 2 sentences using ntlk module and returns.

    sentence1: A subtitle!!
    sentence2: Preferably a text sentence
    Returns: cosine - similarity coefficient, 0 <= cosine <= 1
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

    for subtitle in subtitle_list:
        similarity = compare_2_sentences(subtitle, citiation)
        if similarity > 0.8:
            return (subtitle.start.total_seconds(), subtitle.end.total_seconds())
    
    return 'No citiation present in a movie'


if __name__ == '__main__':
    from srt_wrkwith import return_sub_list, read_data
    from vlc_wrkwith import Player
    main_folder = path.dirname(__file__)
    movie_folder = path.join(main_folder, 'movies')
    p = Player(path.join(movie_folder, 'the_lil_prince.mp4'))
    # print(read_text('lil_prince.txt'))
    # print(compare_subt_w_txt(return_sub_list(read_data('lil_prince_subtitles.srt')) ,read_text('lil_prince.txt')))
    strt, end = check_for_presence('I shall command it.', return_sub_list(read_data('lil_prince_subtitles.srt')))
    # p.play_a_part(int(round(strt, 0)), int(round(end - strt, 0)))
    # print(strt, end)

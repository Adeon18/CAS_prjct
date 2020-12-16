'''
This module is responsible for reading 2 huge csv files data.tsv and names.csv
and finding the adaptations of a book if there is one.
'''
import pandas as pd
from os import path

main_folder = path.dirname(__file__)
info_folder = path.join(main_folder, 'text_info')

def get_all_movies(path_to_file=path.join(info_folder, 'data.tsv')) -> pd.DataFrame:
    '''
    Read the data.tsv file and return the dataframe with only movie names.
    '''
    df = pd.read_csv(path_to_file, delimiter='\t', usecols=['titleType', 'primaryTitle'])
    df = df.loc[df['titleType'] == 'movie']
    # df = df['primaryTitle']
    return df

def get_all_literature(path_to_file=path.join(info_folder, 'names.csv')) -> pd.DataFrame:
    '''
    Read the data.tsv file and return the dataframe with only movie names.
    '''
    df = pd.read_csv(path_to_file, delimiter=',', usecols=['Title'])
    return df


def find_adaptations() -> pd.DataFrame:
    '''
    Compare the lierature dataframe from get_all_literarure and movies
    daaframe from get_all_movies and return the adaptations dataframe.
    '''
    df_movies = get_all_movies()
    df_liter = get_all_literature()
    df = df_movies[df_movies['primaryTitle'].isin(df_liter['Title'])].reset_index()
    return df


if __name__ == '__main__':
    print(find_adaptations())

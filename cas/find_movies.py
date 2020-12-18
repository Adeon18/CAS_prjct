'''
This module is responsible for working with specific data sets.

It can read a file with literature and a file with films and return
the literature adaptations.

Functions:
    get_all_movies
    get_all_literature
    find_adaptations
'''
from os import path
import pandas as pd


def get_all_movies(path_to_file='data.tsv') -> pd.DataFrame:
    '''
    Read the data.tsv file and return the dataframe with only movie names.

    Args:
        path_to_file: The file we read info from(data.tsv by default)
    
    Returns:
        The only dataframe column with movie names
    '''
    df = pd.read_csv(path_to_file, delimiter='\t', usecols=['titleType', 'primaryTitle'])
    df = df.loc[df['titleType'] == 'movie']
    # df = df['primaryTitle']
    return df


def get_all_literature(path_to_file='names.csv') -> pd.DataFrame:
    '''
    Read the names.csv file and return the dataframe with only literature titles.

    Args:
        path_to_file: The file we read info from(names.csv by default)
    
    Returns:
        The only dataframe column with literature titles
    '''
    df = pd.read_csv(path_to_file, delimiter=',', usecols=['Title'])
    return df


def find_adaptations(df_movies: pd.DataFrame, df_liter: pd.DataFrame) -> pd.DataFrame:
    '''
    Compare the lierature dataframe from get_all_literarure and movies
    dataframe from get_all_movies and return the adaptations dataframe.

    Args:
        df_movies: Dataframe with only movies
        df_liter: Dataframe with only literarture

    Retuns:
        A dataframe with all the book adaptations.
    '''
    df = df_movies[df_movies['primaryTitle'].isin(df_liter['Title'])].reset_index()
    return df


if __name__ == '__main__':
    main_folder = path.dirname(__file__)
    data_folder = path.join(main_folder, 'data')
    print(find_adaptations(get_all_movies(path.join(data_folder, 'data.tsv')),
          get_all_literature(path.join(data_folder, 'names.csv'))))

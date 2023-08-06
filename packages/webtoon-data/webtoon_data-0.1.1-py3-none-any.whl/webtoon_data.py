from configparser import ConfigParser
import pandas as pd
import requests
import json

# access
config = ConfigParser()
config.read('config.ini')
api_host = config.get('api', 'host')
api_key = config.get('api', 'key')


# Get a list of genres available on WEBTOON
def get_webtoon_genre_list():
    url = "https://webtoon.p.rapidapi.com/originals/genres/list"
    querystring = {
        "language": "en"
    }
    headers = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }

    response_gen = requests.request("GET", url, headers=headers, params=querystring)  # get request
    webtoon_gen_json = response_gen.json()  # turn into .json format
    webtoon_json_gen_df = pd.DataFrame(webtoon_gen_json['message']['result']['genreList']['genres'])  # into DataFrame
    print(webtoon_json_gen_df['name'].tolist())  # print list of genres obtained


# Get string title of WEBTOON from number ID
def get_webtoon_title(num):
    url_title = "https://webtoon.p.rapidapi.com/originals/titles/get-info"
    headers_title = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }
    querystring_title = {
        "titleNo": num,
        "language": "en"
    }
    # for titles
    response_titles = requests.request("GET", url_title, headers=headers_title, params=querystring_title)  # get req
    response_titles_json = response_titles.json()  # into .json format
    title_json = response_titles_json['message']['result']['titleInfo']['title']  # locate title within json
    return title_json

# function for finding the number of a webtoon title that you already know
def get_webtoon_num(title):
    url_title = "https://webtoon.p.rapidapi.com/originals/titles/list"
    headers_title = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }
    querystring_title = {
        'language': 'en'
    }
    # for the list of WEBTOONs
    response_list = requests.request("GET", url_title, headers=headers_title, params=querystring_title)  # get req
    response_list_json = response_list.json()  # into .json format
    response_list_df = pd.DataFrame(response_list_json['message']['result']['titleList']['titles'])  # df of titles
    title_df = response_list_df[response_list_df['title'] == title]  # create 1-row df corresponding to title

    #( figure out how to ignore case for the title since nobody ever thinks about that)

    if title_df.empty:
        print('I couldn\'t find that title in the list of Originals, please make sure the title is an Original or '
              'check your spelling')
    else:
        print('The title number for (that WEBTOON) is ' + str(title_df['titleNo'].iloc[0]) +
              ', hope that helps! :)')

# get_webtoon_num('True Beauty')

# Get a list of given genre of top ranked WEBTOONS up to placement stated in count
# i.e. get_webtoon_list_ranking('ALL', 23) should result in 23 top WEBTOONs across all genres
def get_webtoon_list_ranking(genre, count):
    url = "https://webtoon.p.rapidapi.com/originals/titles/list-by-rank"
    headers = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }
    querystring = {
        "count": count,
        "language": "en"
    }
    # for rankings
    response_rank = requests.request("GET", url, headers=headers, params=querystring)
    webtoon_rank_json = response_rank.json()
    webtoon_json_rank_df = pd.DataFrame(webtoon_rank_json['message']['result']['titleNoListByTabCode'])
    # print(webtoon_json_rank_df.head())
    # print(webtoon_json_rank_df['tabCode'])
    ranked_list = webtoon_json_rank_df.loc[webtoon_json_rank_df['tabCode'] == genre]['titleNoList'].tolist()
    # print(ranked_list)
    rank_list = ranked_list[0]
    # print(rank_list)

    ranked_title_list = []  # initiate empty list for ranked list
    for rank in rank_list:
        ranked_title_list.append(get_webtoon_title(rank))  # replace number titles with string titles, readability
    return print(ranked_title_list)

# get_webtoon_list_ranking('ROMANCE', 25)


# Provide 3 WEBTOON recommendations based on title provided
# AND ALSO PROVIDE A SUMMARY OF EACH ONE (DESCRIPTION)
def get_recommendations(title_number):
    url_rec = "https://webtoon.p.rapidapi.com/originals/titles/get-recommend"
    querystring_rec = {
        "titleNo": title_number,
        "language": "en"
    }
    headers_rec = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }

    response_rec = requests.request("GET", url_rec, headers=headers_rec, params=querystring_rec)
    response_rec_json = response_rec.json()  # turn it into json
    response_rec_df = pd.DataFrame(response_rec_json['message']['result']['recommend'])  # [0]['webtoon']

    # print(response_rec_df.head())

    if response_rec_df.empty:
        print('I can\'t find that one, pls check your ID again or add a different WEBTOON - I can take another look :O')
    else:
        rec_df = pd.DataFrame(response_rec_json['message']['result']['recommend'][0]['webtoon'])
        all_recs_df = rec_df[['title', 'titleNo', 'representGenre', 'writingAuthorName', 'pictureAuthorName',
                              'language', 'starScoreAverage', 'readCount', 'favoriteCount', 'synopsis']]
        print('Here are three WEBTOONs that we recommend if you enjoy ' + get_webtoon_title(title_number) + ':')
        print(all_recs_df)

# get_recommendations(1436)


# Get a list of genres available on WEBTOON
def get_webtoon_genre_list_c():
    url = "https://webtoon.p.rapidapi.com/canvas/genres/list"
    querystring = {
        "language": "en"
    }
    headers = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }

    response_gen = requests.request("GET", url, headers=headers, params=querystring)  # get request
    webtoon_gen_json = response_gen.json()  # turn into .json format
    webtoon_json_gen_df = pd.DataFrame(webtoon_gen_json['message']['result']['genreTabList']['genreTabs'])  # into DataFrame
    print(webtoon_json_gen_df['name'].tolist())  # print list of genres obtained


# Get string title of WEBTOON from number ID
def get_webtoon_title_c(num):
    url_title = "https://webtoon.p.rapidapi.com/canvas/titles/get-info"
    headers_title = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }
    querystring_title = {
        "titleNo": num,
        "language": "en"
    }
    # for titles
    response_titles = requests.request("GET", url_title, headers=headers_title, params=querystring_title)  # get req
    response_titles_json = response_titles.json()  # into .json format
    title_json = response_titles_json['message']['result']['titleInfo']['title']  # locate title within json
    return title_json

# function for finding the number of a webtoon title that you already know
def get_webtoon_num_c(title):
    url_title = "https://webtoon.p.rapidapi.com/canvas/titles/list"
    headers_title = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }
    querystring_title = {
        'language': 'en'
    }
    # for the list of WEBTOONs
    response_list = requests.request("GET", url_title, headers=headers_title, params=querystring_title)  # get req
    response_list_json = response_list.json()  # into .json format
    response_list_df = pd.DataFrame(response_list_json['message']['result']['titleList']['titles'])  # df of titles
    title_df = response_list_df[response_list_df['title'] == title]  # create 1-row df corresponding to title

    #( figure out how to ignore case for the title since nobody ever thinks about that)

    if title_df.empty:
        print('I couldn\'t find that title on Canvas, please make sure the title is on Canvas or '
              'check your spelling')
    else:
        print('The title number for (that WEBTOON) is ' + str(title_df['titleNo'].iloc[0]) +
              ', hope that helps! :)')

# get_webtoon_num('The Little Trashmaid')


# Provide 3 WEBTOON recommendations based on title provided
# AND ALSO PROVIDE A SUMMARY OF EACH ONE (DESCRIPTION)
def get_recommendations_c(title_number):
    url_rec = "https://webtoon.p.rapidapi.com/canvas/titles/get-recommend"
    querystring_rec = {
        "titleNo": title_number,
        "language": "en"
    }
    headers_rec = {
        'x-rapidapi-host': api_host,
        'x-rapidapi-key': api_key
    }

    response_rec = requests.request("GET", url_rec, headers=headers_rec, params=querystring_rec)
    response_rec_json = response_rec.json()  # turn it into json
    response_rec_df = pd.DataFrame(response_rec_json['message']['result']['recommendMap']['VIEWER_VIEW_TITLE_READ_TITLE']['titleList'])  # [0]['webtoon']

    # print(response_rec_df.head())

    if response_rec_df.empty:
        print('I can\'t find that one, pls check your ID again or add a different WEBTOON - I can take another look :O')
    else:
        rec_df = pd.DataFrame(response_rec_json['message']['result']['recommendMap']['VIEWER_VIEW_TITLE_READ_TITLE']['titleList'])
        all_recs_df = rec_df[['title', 'titleNo', 'genre', 'language', 'writingAuthorName', 'pictureAuthorName']]
        print('Here are some WEBTOONs that we recommend if you enjoy ' + get_webtoon_title_c(title_number) + ':')
        print(all_recs_df)

get_recommendations_c(300138)
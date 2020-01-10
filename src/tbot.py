import twitter
import json
import csv
import pandas as pd


csv_file = 'tweets.csv'
key_file = 'keys.json'


def loadSuperSecretKeys(key_file):
    file = key_file
    with open(file, 'r') as f:
        superSecrets = json.load(f)
    return superSecrets


def loadTwit(superSecrets):
    api = twitter.Api(consumer_key=superSecrets["consumer_key"],
                      consumer_secret=superSecrets["consumer_secret"],
                      access_token_key=superSecrets["access_token_key"],
                      access_token_secret=superSecrets["access_token_secret"])
    return api


def searchTwit(api: object, keyword: str):  # get tweets from past 7 days. You get what you pay for -> nothing.
    search = api.GetSearch(keyword)
    for tweet in search:
        yield {tweet.id: tweet.text.encode('utf-8')}


def saveTwits(dict, csv_file, list):
    with open(csv_file, 'a', encoding='utf8') as csv:
        for k, v in dict.items():
            if k not in list:
                csv.write('"' + str(k) + '","' + str(v).replace(',', '') + '"\n')


def readTwitIDs(csv_file):
    idList = []
    df = pd.read_csv(csv_file)
    for column in df.iterrows():
        idList.append(column[1][0])
    return idList


def analyzeTwits(csv_file):
    text = ''
    df = pd.read_csv(csv_file)
    for column in df.iterrows():
        text = text + ' ' + str(column[1][1])
    return text.replace('.', '').replace(',', '').replace('#', '').replace('"', '').replace('@', '').replace('!',
                                                                                                             '').replace(
        ':', '').replace('?', '').replace("b'rt", ' ').replace(' to ', '').replace(' a ', ' ').replace(' and ',
                                                                                                       '').replace(
        ' as ', '').replace(' you ', '').replace(' for ', '')


def main():
    idList = readTwitIDs(csv_file)
    superSecrets = loadSuperSecretKeys(key_file)
    api = loadTwit(superSecrets)
    tweeties = searchTwit(api)
    for t in tweeties:
        saveTwits(t, csv_file, idList)
    text = analyzeTwits(csv_file)
    #do something with text


if __name__ == '__main__':  # <-allows import of file in other projects without executing code.
    main()
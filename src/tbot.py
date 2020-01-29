import twitter
import json
import csv
import pandas as pd


class TwitBot:
    def __init__(self, csv_file: str, key_file: str):
        self.csv_file = csv_file
        self.key_file = key_file
        self.super_secrets = None
        self.api = None
        self.id_list = []

    def load_super_secret_keys(self):
        with open(self.key_file, 'r') as f:
            ss = json.load(f)
        self.super_secrets = ss

    def load_twit(self):
        self.api = twitter.Api(consumer_key=self.super_secrets["consumer_key"],
                                  consumer_secret=self.super_secrets["consumer_secret"],
                                  access_token_key=self.super_secrets["access_token_key"],
                                  access_token_secret=self.super_secrets["access_token_secret"])

    def search_twit(self, keyword: str):  # get tweets from past 7 days. You get what you pay for -> nothing.
        search = self.api.GetSearch(keyword)
        for tweet in search:
            yield {tweet.id: tweet.text.encode('utf-8')}

    def save_twits(self, dict):
        with open(self.csv_file, 'a', encoding='utf8') as csv:
            for k, v in dict.items():
                if k not in self.id_list:
                    csv.write('"' + str(k) + '","' + str(v).replace(',', '') + '"\n')

    def read_current_twit_ids(self):
        df = pd.read_csv(self.csv_file)
        for column in df.iterrows():
            self.id_list.append(column[1][0])

    def analyze_twits(self):
        text = ''
        df = pd.read_csv(self.csv_file)
        for column in df.iterrows():
            text = text + ' ' + str(column[1][1])
        return text.replace('.', '').replace(',', '').replace('#', '').replace('"', '').replace('@', '').replace('!',
                                                                                                                 '').replace(
            ':', '').replace('?', '').replace("b'rt", ' ').replace(' to ', '').replace(' a ', ' ').replace(' and ',
                                                                                                           '').replace(
            ' as ', '').replace(' you ', '').replace(' for ', '')


def main():
    csv_file = 'tweets.csv'
    key_file = 'keys.json'
    t = TwitBot(csv_file, key_file)
    t.load_super_secret_keys()
    t.load_twit()
    tweeties = t.search_twit('quantum biology')
    #t.read_current_twit_ids()
    for t in tweeties:
        print(t)



if __name__ == '__main__':  # <-allows import of file in other projects without executing code.
    main()
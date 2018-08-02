import time
import csv
import codecs
import requests
import sqlite3
import sys
from time import sleep
from configparser import ConfigParser
from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup
from dbconnector import DatabaseConnector
from dataanalyzer import DataAnalyzer

class APIconnector():

    def __init__(self, f):
        self.current_time = self.current_time()
        self.batchID = self.get_batch_id()
        self.steam = self.get_steam_data(fetch=f)
        self.twitch = self.get_twitch_data(fetch=f)


    def get_batch_id(self):
        with codecs.open("batch", 'r') as batch:
            lines = batch.readlines()
            if len(lines) < 1:
                last_batch = False
            else:
                last_batch = lines[-1]

        with codecs.open("batch", 'a') as batch:
           if last_batch:
               batch.write(str(int(last_batch) + 1) + "\n")
               return last_batch
           else:
               last_batch = 1
               batch.write("1\n")
               return last_batch


    def current_time(self):
        timestamp = time.time()
        current_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return current_time


    def config(self, section, filename='conf.ini'):
        parser = ConfigParser()
        parser.read(filename)
        conf = {}

        if parser.has_section(section):
            parameters = parser.items(section)
            for param in parameters:
                conf[param[0]] = param[1]
        else:
            raise Exception("config not found!")

        return conf


    def get_steam_data(self, fetch=True):
        # based on https://gist.github.com/JonLim/985acb4b8d58fa5b154a
        steampage = BeautifulSoup(urlopen('http://store.steampowered.com/stats/?l=english').read(), 'html.parser')
        current_players = {}
        if fetch:
            with codecs.open('steamtop100.csv', 'w') as top100:
                writer = csv.writer(top100, delimiter='\t', lineterminator='\n')
                for row in steampage('tr', {'class': 'player_count_row'}):
                    current_row = []
                    steam_app_id = row.a.get('href').split("/")[4]
                    game_name = row.a.get_text()
                    concurrent_players = row.find_all('span')[0].get_text().replace(",","")
                    current_row.extend([self.current_time, steam_app_id, game_name, concurrent_players, self.batchID])
                    # maxConcurrent = row.find_all('span')[1].get_text().replace(",","")
                    writer.writerow(current_row)
                    current_players[game_name] = concurrent_players
        else:
            with codecs.open('steamtop100.csv') as src:
                reader = csv.reader(src, delimiter='\t', lineterminator='\n')
                for row in reader:
                    current_players[row[2]] = row[3]

        return current_players

    def get_twitch_data(self, fetch=True):
        request_url = 'https://api.twitch.tv/helix/games/top'
        conf = self.config(section='twitch')
        headers = {'Accept': 'application/vnd.twitchtv.v5+json',
                   'Client-ID': conf['client_id']}
        game_url = 'https://api.twitch.tv/helix/streams?game_id='
        viewers_by_game = {}

        if fetch:
            res = requests.get(request_url, headers=headers)
            data = res.json()
            with codecs.open('twitchtop.csv', 'w') as twitchtop:
                for x in data['data']:
                    writer = csv.writer(twitchtop, delimiter='\t', lineterminator='\n')
                    name = x['name']
                    viewers_by_game[name] = 0
                    game_data_url = game_url + str(x['id'])
                    print(game_data_url)
                    game_data = requests.get(game_data_url, headers=headers).json()
                    for game in game_data['data']:
                        viewers_by_game[name] += game['viewer_count']
                    writer.writerow([self.current_time, name, viewers_by_game[name], self.batchID])

        else:
            with codecs.open('twitchtop.csv', 'r') as twitchtop:
                reader = csv.reader(twitchtop, delimiter='\t', lineterminator='\n')
                for row in reader:
                    viewers_by_game[row[1]] = row[2]

        return viewers_by_game

def fetch_data():
        ac = APIconnector(True)
        dbconnector = DatabaseConnector(steam=ac.steam, twitch=ac.twitch, current_time=ac.current_time, batchID=ac.batchID)
        dbconnector.create_schema()
        dbconnector.insert_data()

def plot_data():
        da = DataAnalyzer()
        # da.show()
        da.plot_data()
        da.plot_ratio()
        da.plot_order()

if __name__ == "__main__":
    if len(sys.argv) > 3:
        fetch = sys.argv[1]
        plot = sys.argv[2]
        fetch_timer = int(sys.argv[3])
        while True:
            if fetch == '1':
                fetch_data()
            if plot == '1':
                plot_data()
            sleep(fetch_timer)

    else:
        print("no arguments given, fetching and plotting")
        print("example arg: get_data.py 1 1 900 (fetches and plots data, fetches new data every 15 minutes)")
        print("example arg: get_data.py 1 0 900 (fetches, fetches new data every 15 minutes)")
        fetch_data()
        plot_data()

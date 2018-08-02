import sys
from APIconnector import APIconnector
from data_analyzer import DataAnalyzer
from dbconnector import DatabaseConnector
from time import sleep


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

def init_fetching():
    if len(sys.argv) > 3:
        fetch = sys.argv[1]
        plot = sys.argv[2]
        fetch_timer = int(sys.argv[3])
        if fetch_timer != 0:
            while True:
                if fetch == '1':
                    fetch_data()
                if plot == '1':
                    plot_data()
                sleep(fetch_timer)
        else:
            if fetch == '1':
                fetch_data()
            if plot == '1':
                plot_data()

    else:
        print("no arguments given, fetching and plotting")
        print("example arg: get_data.py 1 1 900 (fetches and plots data, fetches new data every 15 minutes)")
        print("example arg: get_data.py 1 0 900 (fetches, fetches new data every 15 minutes)")
        fetch_data()
        plot_data()

if __name__ == "__main__":
    init_fetching()

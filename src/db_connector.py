import sqlite3


class DatabaseConnector():


    def __init__(self, steam=None, twitch=None, current_time=None, batchID=None):
        self.steam = steam
        self.twitch = twitch
        self.current_time = current_time
        self.batchID = batchID
        self.database = 'playerdb.db'
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()


    def create_schema(self):
        #try:
        steam_players_cmd = """CREATE TABLE IF NOT EXISTS current_players(
                        timestamp DATETIME,
                        batchID INTEGER,
                        game TEXT,
                        players INTEGER,
                        PRIMARY KEY(batchID, game));
                        """
        twitch_watchers_cmd = """CREATE TABLE IF NOT EXISTS current_watchers (
                        timestamp DATETIME,
                        batchID INTEGER,
                        game TEXT,
                        players INTEGER,
                        PRIMARY KEY(batchID, game));
                        """
        self.cursor.execute(steam_players_cmd)
        self.cursor.execute(twitch_watchers_cmd)
        self.connection.commit()


    def insert_data(self):
        insert_cmd_twitch = """INSERT INTO current_watchers VALUES (?, ?, ?, ?);"""
        insert_cmd_steam = """INSERT INTO current_players VALUES (?, ?, ?, ?);"""
        #try:
        for element in self.steam:
            values = [self.current_time, self.batchID, element, self.steam[element]]
            self.cursor.execute(insert_cmd_steam, values)

        for element in self.twitch:
            values = [self.current_time, self.batchID, element, self.twitch[element]]
            self.cursor.execute(insert_cmd_twitch, values)

        self.connection.commit()

        print("inserted batch " + self.batchID.strip("\n") + " at " + self.current_time)

    def fetch_data(self, query):
        return self.cursor.execute(query).fetchall()

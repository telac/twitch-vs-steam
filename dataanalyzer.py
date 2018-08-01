from dbconnector import DatabaseConnector
from plotly.offline import plot
import plotly.graph_objs as go
import queries


class DataAnalyzer():
    def __init__(self):
        self.dbconnector = DatabaseConnector()
        self.dataset = self.dbconnector.fetch_data(query=queries.queries('compare'))
        self.unique = self.dbconnector.fetch_data(query=queries.queries('uniquecompare'))

    def show(self):
        for row in self.dataset:
            print(row)
            ratio = row[4]/row[3]
            print("comparison data steam/twitch: " + str(ratio))

    def plot_data(self):
        traces = []
        for unique in self.unique:
            unique = unique[0]
            steam_x=[]
            steam_y=[]
            twitch_x=[]
            twitch_y=[]
            for row in self.dataset:
                if unique == row[2]:
                    steam_x.append(row[1])
                    steam_y.append(row[4])
                    twitch_x.append(row[1])
                    twitch_y.append(row[3])

            traces.append(self.construct_trace(unique + ' steam ', steam_x, steam_y))
            traces.append(self.construct_trace(unique + ' twitch ', twitch_x, twitch_y))

        plot(traces, filename='raw_data.html')

    def plot_ratio(self):
        traces = []
        for unique in self.unique:
            unique = unique[0]
            x = []
            y = []
            for row in self.dataset:
                if unique == row[2]:
                    x.append(row[1])
                    y.append(row[4]/row[3])

            traces.append(self.construct_trace(unique + ' ratio [steam/twitch]', x, y))

        plot(traces, filename='ratios.html')


    def construct_trace(self, name0, x0, y0):
        trace = go.Scatter(
            x = x0,
            y = y0,
            name=name0,
            mode='lines'
        )
        return trace

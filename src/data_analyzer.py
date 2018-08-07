import plotly.graph_objs as go
import queries
from db_connector import DatabaseConnector
from plotly.offline import plot


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

            traces.append(self.construct_trace('[steam] ' + unique, steam_x, steam_y))
            traces.append(self.construct_trace('[twitch] ' + unique, twitch_x, twitch_y))

        plot(traces, filename='../plots/raw_data.html')

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

        plot(traces, filename='../plots/ratios.html')


    def plot_order(self):
        # this has to be fixed sometime. for now it works, but is ugly.
        traces = []
        for unique in self.unique:
            unique = unique[0]
            x = []
            y = []
            x_s = []
            y_s = []
            for row in self.dataset:
                twitch_dict = {}
                steam_dict = {}
                if unique == row[2]:
                    batch_id = row[0]
                    for row in self.dataset:
                        if row[0] == batch_id:
                            twitch_dict[row[2]] = [row[1], row[3]]
                            steam_dict[row[2]] = [row[1], row[4]]
                    sorted_y = sorted(twitch_dict.items(), key=lambda kv: kv[1][1])
                    sorted_y_steam = sorted(steam_dict.items(), key=lambda kv: kv[1][1])
                    for index, value in enumerate(sorted_y):
                        if value[0] == unique:
                            x.append(value[1][0])
                            y.append(index + 1)

                    for index, value in enumerate(sorted_y_steam):
                        if value[0] == unique:
                            x_s.append(value[1][0])
                            y_s.append(index + 1)

            traces.append(self.construct_trace('[twitch]' + unique + '  order', x, y))
            traces.append(self.construct_trace('[steam]' + unique + '  order', x_s, y_s))

        plot(traces, filename='../plots/order.html')


    def construct_trace(self, name0, x0, y0):
        trace = go.Scatter(
            x = x0,
            y = y0,
            name=name0,
            mode='lines',
            text= [str(name0 + ' : ' + str(y_)) for y_ in y0],
            hoverinfo='text'
        )
        return trace

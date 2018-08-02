Fetches data from twitch viewers and from steam to compare twitch viewership vs amount of players in steam per game.

Dependencies

`plotly`, `requests` and `BeautifulSoup`

# How to install dependencies:

```
pip install beautifulsoup4
pip install requests
pip install plotly
```

# How to use:

Run `get_data`. Running `get_data` again incrementally adds data with timestamps to a `sqilite3` database, where the data is then plotted from.

You can also provide arguments:

`get_data.py [FETCH] [PLOT] [TIMER]`

##### parameters
* `[FETCH] = 1` fetches data, other values ignore the fetching portion.
* `[PLOT] = 1` plots data and, other values ignore the plotting portion.
* `[TIMER]` sets a which runs the program every `n` seconds. `0` only runs the program once.

##### examples:

* `get_data.py 1 0 900` fetches data every 15 minutes, but does not plot the data on each iteration.
* `get_data.py 0 1 0` does *not* fetch data, plots data but only once.
* `get_data.py` with no parameters fetches latest data, plots all three plots and then exits.


You will also need to create a `conf.ini` file that contains at least the following:
```
[twitch]
client_id=<your twitch API-key>
```

# Current Plots

[raw data](plots/raw_data.html)

[ratios](plots/ratios.html)

[order](plots/order.html)

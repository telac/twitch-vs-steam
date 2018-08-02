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

You will also need to create a `conf.ini` file that contains at least the following:
```
[twitch]
client_id=<your twitch API-key>
```

# Current Plots

[raw data](plots/raw_data.html)

[ratios](plots/ratios.html)

[order](plots/order.html)

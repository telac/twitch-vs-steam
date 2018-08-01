Fetches data from twitch viewers and from steam to compare twitch viewership vs amount of players in steam per game.

Dependencies

`plotly` and `BeautifulSoup`

How to use:

Run `get_data`. Running `get_data` again incrementally adds data with timestamps to a `sqilite3` database, where the data is then plotted from.

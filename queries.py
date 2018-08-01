def queries(query):
    queries = {'compare' : """SELECT s.batchID, s.timestamp, s.game, t.players, s.players
                FROM current_players s
                INNER JOIN current_watchers t
                ON s.batchID = t.batchID AND s.game = t.game;
                """,
                'uniquecompare' : """
                SELECT DISTINCT GAME FROM (
                SELECT s.timestamp, s.game, t.players, s.players
                FROM current_players s
                INNER JOIN current_watchers t
                ON s.batchID = t.batchID AND s.game = t.game);
                """
                }

    return queries[query]

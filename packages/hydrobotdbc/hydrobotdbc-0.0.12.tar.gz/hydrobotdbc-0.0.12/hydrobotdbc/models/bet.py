from ..client import Client
from .collection import Collection


class Bet:
    __tablename__ = 'BetHistory'

    class Query:
        def __init__(self):
            self.client = Client()

        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM BetHistory WHERE GameId={id}")

            return None if row is None else Bet(row.BetId, row.DiscordId, row.SeedId, row.GameId, row.BetAmount, row.RewardAmount, row.DateRecAdded)

        def filter_by(self, bet_id=None, discord_id=None, game_id=None):
            sql = f"SELECT * FROM BetHistory "

            allow_multi_clause = False
            if bet_id is not None:
                sql += f"WHERE GameId={bet_id} "
                allow_multi_clause = True
            if discord_id is not None:
                sql += f"AND DiscordId='{discord_id}' " if allow_multi_clause else f"WHERE DiscordId='{discord_id}' "
                allow_multi_clause = True
            if game_id is not None:
                sql += f"AND GameId='{game_id}' " if allow_multi_clause else f"WHERE GameId='{game_id}' "


            sql += "ORDER BY DateRecAdded Desc"

            rows = self.client.exec_fetchall(sql)

            bets = []
            for row in rows:
                bets.append(Bet(row.BetId, row.DiscordId, row.SeedId, row.GameId, row.BetAmount, row.RewardAmount, row.DateRecAdded))

            return Collection(bets)

    query = Query()

    def __init__(self, discord_id, seed_id, game_id, bet_amount, reward_amount):
        self.BetId = None
        self.DiscordId = discord_id
        self.SeedId = seed_id
        self.GameId = game_id
        self.BetAmount = bet_amount
        self.RewardAmount = reward_amount
        self.DateRecAdded = None

    @property
    def id(self):
        return self.BetId

    @property
    def discordId(self):
        return self.DiscordId

    @property
    def seedId(self):
        return self.SeedId

    @property
    def gameId(self):
        return self.GameId

    @property
    def bet_amount(self):
        return self.BetAmount

    @property
    def reward_amount(self):
        return self.RewardAmount

    @property
    def date_rec_added(self):
        return self.DateRecAdded

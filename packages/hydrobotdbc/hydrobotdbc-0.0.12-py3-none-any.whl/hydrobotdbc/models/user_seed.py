from ..client import Client
from .collection import Collection

class UserSeed:
    __tablename__ = 'UserSeeds'
    class Query:
        def __init__(self):
            self.client = Client()

        def get(self, discord_id: int):
            row = self.client.exec_fetchone(f"SELECT TOP 1 * FROM UserSeeds WHERE DiscordId={discord_id} AND Displayed=0 ORDER BY SeedId DESC")

            return None if row is None else UserSeed(row.Seed, row.DiscordId, row.Nonce, row.Displayed)

        def filter_by(self, seed=None, discord_id=None, displayed=None):
            sql = "SELECT * FROM UserSeeds "

            allow_multi_clause = False
            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id} "
                allow_multi_clause = True
            if displayed is not None:
                sql += f"AND Displayed={displayed}" if allow_multi_clause else f"WHERE Displayed={displayed}"
                allow_multi_clause = True
            if seed is not None:
                sql += f"AND Seed={seed}" if allow_multi_clause else f"WHERE Seed={seed}"

            rows = self.client.exec_fetchall(sql)

            seeds = []
            for row in rows:
                seeds.append(UserSeed(row.Seed, row.DiscordId, row.Nonce, row.Displayed))

            return Collection(seeds)

    query = Query()

    def __init__(self, seed, discord_id, nonce, displayed):
        self.SeedId = None
        self.Seed = seed
        self.DiscordId = discord_id
        self.Nonce = nonce
        self.Displayed = displayed
        self.DateRecAdded = None

    @property
    def id(self):
        return self.SeedId

    @property
    def seed(self):
        return self.Seed

    @property
    def discordId(self):
        return self.DiscordId

    @property
    def nonce(self):
        return self.Nonce

    @property
    def displayed(self):
        return self.Displayed

    @property
    def date_rec_added(self):
        return self.DateRecAdded
from ..client import Client
from .collection import Collection


class Game:
    __tablename__ = 'Games'

    class Query:
        def __init__(self):
            self.client = Client()

        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM Games WHERE GameId={id}")

            return None if row is None else Game(row.GameId, row.Name, row.Description, row.DateRecAdded)

        def filter_by(self, game_id=None, name=None):
            sql = "SELECT * FROM Games "

            if game_id is not None:
                sql += f"WHERE GameId={game_id} "
            elif name is not None:
                sql += f"WHERE Name='{name}' "

            sql += "ORDER BY GameId ASC"

            rows = self.client.exec_fetchall(sql)

            games = []
            for row in rows:
                games.append(Game(row.GameId, row.Name, row.Description, row.DateRecAdded))

            return Collection(games)

    query = Query()

    def __init__(self, name, description):
        self.GameId = None
        self.Name = name
        self.Description = description
        self.DateRecAdded = None

    @property
    def id(self):
        return self.GameId

    @property
    def name(self):
        return self.Name

    @property
    def description(self):
        return self.Description


    @property
    def date_rec_added(self):
        return self.DateRecAdded

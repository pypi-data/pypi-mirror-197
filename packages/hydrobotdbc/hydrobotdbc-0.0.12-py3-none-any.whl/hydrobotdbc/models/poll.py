from ..client import Client
from .collection import Collection

class Poll:
    __tablename__ = 'PollsQueue'
    class Query:
        def __init__(self):
            self.client = Client()

        def get(self):
            row = self.client.exec_fetchone(f"SELECT * FROM PollsQueue WHERE PollId={id}")

            return None if row is None else Poll(row.PollId, row.DiscordId, row.Title, row.Options, row.DateRecAdded)

        def filter_by(self, discord_id=None):
            sql = "SELECT * FROM PollsQueue "

            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id}"

            sql += "ORDER BY DateRecAdded ASC"

            rows = self.client.exec_fetchall(sql)

            polls = []
            for row in rows:
                polls.append(Poll(row.PollId, row.DiscordId, row.Title, row.options, row.DateRecAdded))

            return Collection(polls)

    query = Query()

    def __init__(self, discord_id, title, options):
        self.PollId = None
        self.DiscordId = discord_id
        self.Title = title
        self.Options = options
        self.DateRecAdded = None

    @property
    def id(self):
        return self.PollId

    @property
    def discordId(self):
        return self.DiscordId

    @property
    def title(self):
        return self.Title

    @property
    def options(self):
        return self.Options

    @property
    def date_rec_added(self):
        return self.DateRecAdded
# app/db/models.py

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def query_get(id):
        # fake database lookup
        if id == 1:
            return Player(1, "Test Player")
        return None


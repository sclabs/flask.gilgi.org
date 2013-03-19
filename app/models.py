from app import db

class Dota2Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer)
    rating = db.Column(db.String(10))

    def __init__(self, team_id, rating='inactive'):
        self.team_id = team_id
        self.rating = rating

    def __repr__(self):
        return '<team_id ' + str(self.team_id) + '>'

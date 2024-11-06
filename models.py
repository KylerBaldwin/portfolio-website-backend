from app import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name
        }
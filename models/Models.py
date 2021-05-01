from models import db
import pymysql as MySQLdb
class Disease(db.Model):
    __table__name = "diseases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    symptoms = db.Column(db.Text(), nullable=False)
    causes = db.Column(db.Text(), nullable=False)
    solutions = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text(), nullable=False)

class Feedback(db.Model):
    __table__name = "feedbacks"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Text(), nullable=False)
    disease = db.Column(db.Text(), nullable=False)

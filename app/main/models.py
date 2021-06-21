from sqlalchemy import Column, Integer, String, DateTime
from .. import db

# Event Model
class Events(db.Model):
    __tablename__ = 'Events'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    venue = Column(String)
    dates = Column(DateTime)
    image = Column(String)

# Feed Models
class Feeds(db.Model):
    __tablename__= "Feeds"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    image = Column(String)


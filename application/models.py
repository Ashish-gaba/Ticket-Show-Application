from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

db = SQLAlchemy()

# Explicitly enabling foreign key support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
class Admin(db.Model):
    admin_id = db.Column(db.Integer(), primary_key = True)
    admin_username = db.Column(db.String(16), nullable=False)
    admin_password = db.Column(db.String(16), nullable = False)
    def __repr__(self):
        return "<Admin %r>" %self.admin_username

class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key = True)
    user_username = db.Column(db.String(16), nullable=False)
    user_password = db.Column(db.String(16), nullable = False)
    bookings = db.relationship("Booking", backref = "user", cascade="all, delete")
    def __repr__(self):
        return "<User %r>" %self.user_username

class Venue(db.Model):
    __tablename__ = "venue"
    venue_id = db.Column(db.Integer(), primary_key = True)
    venue_name = db.Column(db.String(20), nullable=False)
    venue_place = db.Column(db.String(20), nullable=False)
    venue_location = db.Column(db.String(20), nullable = False)
    venue_capacity = db.Column(db.Integer(), nullable = False)
    shows = db.relationship("Show", backref="venue", passive_deletes='all')
    def __repr__(self):
        return "<Venue %r>" %self.venue_name

class Show(db.Model):
    __tablename__ = "show"
    show_id = db.Column(db.Integer(), primary_key=True)
    show_name = db.Column(db.String(20), nullable=False)
    show_rating = db.Column(db.Integer(), nullable=False)
    show_start_time = db.Column(db.String(10), nullable=False)
    show_end_time = db.Column(db.String(10), nullable=False)
    show_tags = db.Column(db.String(50), nullable=False)
    show_price = db.Column(db.Integer(), nullable=False)
    show_available_seats = db.Column(db.Integer(), nullable=False)
    show_venue_id = db.Column(db.Integer(), db.ForeignKey("venue.venue_id", ondelete='CASCADE'))
    bookings = db.relationship("Booking", backref="show", passive_deletes='all')
    def __repr__(self):
        return "<Show %r>" %self.show_name

class Booking(db.Model):
    booking_id = db.Column(db.Integer(), primary_key=True)
    booking_tickets_booked = db.Column(db.Integer(), nullable=False)
    booking_show_id = db.Column(db.Integer(), db.ForeignKey("show.show_id", ondelete='CASCADE'))
    booking_user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"), nullable=False)
    def __repr__(self):
        return "<Booking %r>" %self.booking_id


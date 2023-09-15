from datetime import datetime
from rubygymapp import db

class Client(db.Model):
    client_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    client_fname = db.Column(db.String(75),nullable=False)
    client_lname = db.Column(db.String(75),nullable=False)
    client_phone = db.Column(db.String(25),nullable=False)
    client_address =db.Column(db.String(255),nullable=True)
    client_email = db.Column(db.String(100),unique=True) 
    client_pwd = db.Column(db.String(100),unique=True)
    client_subscription =db.Column(db.Enum('monthly','3 months','6 months','annually'),nullable=False,server_default=("monthly"))
    program =db.Column(db.Enum('self','group','private training'),nullable=False,server_default=("self"))
    client_regdate = db.Column(db.DateTime(),default=datetime.utcnow)
    #relationship with Emergency_contact
    emergency_det = db.relationship('Emergency_contact', backref="cdeets", passive_deletes=True)

class Emergency_contact(db.Model):
    emcontact_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    em_fname = db.Column(db.String(75),nullable=False)
    em_lname = db.Column(db.String(75),nullable=False)
    em_phonenum  = db.Column(db.String(25),nullable=False)
    em_address =db.Column(db.String(255),nullable=True)
    #foreign key
    clientID  = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete='CASCADE'))
    #set relationship with Client
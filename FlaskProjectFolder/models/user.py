from FlaskProjectFolder import db


class User(db.Model):
    __tablename__ = "tbl_user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.BigInteger)
    date_registered = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())

    def __init__(self, public_id, username, password, name, email, gender, phone_number):
        self.public_id = public_id
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.gender = gender
        self.phone_number = phone_number

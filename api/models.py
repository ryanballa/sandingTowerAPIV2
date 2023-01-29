from app import db

user_club = db.Table('user_club',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
                    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    isAdmin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)
    memberships = db.relationship('Club', secondary=user_club, backref='users')
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "isAdmin": self.isAdmin,
            "created_at": str(self.created_at.strftime('%d-%m-%Y')),
            "updated_at": str(self.created_at.strftime('%d-%m-%Y')),
            "memberships": self.memberships
        }

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at.strftime('%d-%m-%Y')),
            "updated_at": str(self.created_at.strftime('%d-%m-%Y'))
        }
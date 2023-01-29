from datetime import date
from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import User, Club

@convert_kwargs_to_snake_case
def create_user_resolver(obj, info, name, email):
    try:
        today = date.today()
        user = User(
            name=name, email=email, created_at=today.strftime("%b-%d-%Y")
        )
        db.session.add(user)
        db.session.commit()

        payload = {
            "success": True,
            "user": user.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    except AttributeError as error:
        payload = {
            "success": False,
            "errors": error
        }
    return payload


@convert_kwargs_to_snake_case
def update_user_resolver(obj, info, id, name, email, club_ids):
    def transformClubIds(ids):
        if ids != "":    
            clubIds = ids.split(',')
            return list(map(convertToInt, clubIds))
        return [0]
    
    def convertToInt(n):
        return int(n)
    
    try:
        user = User.query.get(id)
        clubs = db.session.query(Club).filter(Club.id.in_(transformClubIds(club_ids))).all()
        if user:
            user.name = name
            user.email = email
            user.memberships = clubs
            db.session.add(user)
            db.session.commit()
            payload = {
                "success": True,
                "user": user.to_dict()
            }
        if not user:
            payload = {
                "success": False,
                "errors": ["An error occurred when updating"]
            }
    except AttributeError as error:
        payload = {
            "success": False,
            "errors": ["user matching id {id} not found", error]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_user_resolver(obj, info, id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        payload = {"success": True, "user": user.to_dict()}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload
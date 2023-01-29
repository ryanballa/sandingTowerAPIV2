from datetime import date
from ariadne import convert_kwargs_to_snake_case
from api import models
from api import db
from api.models import Club

@convert_kwargs_to_snake_case
def create_club_resolver(obj, info, name, created_at):
    try:
        today = date.today()
        club = Club(
            name=name, created_at=today.strftime("%b-%d-%Y"), updated_at=today.strftime("%b-%d-%Y")
        )
        db.session.add(club)
        db.session.commit()
        payload = {
            "success": True,
            "club": club.to_dict()
        }
    except Exception as error: 
        payload = {
            "success": False,
            "errors": error
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
def update_club_resolver(obj, info, id, name, updated_at):
    try:
        club = Club.query.get(id)
        today = date.today()
        if club:
            club.name = name
            club.updated_at = updated_at, today
            db.session.add(club)
            db.session.commit()
            payload = {
                "success": True,
                "user": club.to_dict()
            }
        if not club:
            payload = {
                "success": False,
                "errors": ["Club not found with id {id}"]
            }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Club matching id {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_club_resolver(obj, info, id):
    try:
        club = Club.query.get(id)
        db.session.delete(club)
        db.session.commit()
        payload = {"success": True, "club": club.to_dict()}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload
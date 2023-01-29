from ..models import Club
from ariadne import convert_kwargs_to_snake_case

@convert_kwargs_to_snake_case
def getClub_resolver(obj, info, id):
    try:
        club = Club.query.get(id)
        payload = {
            "success": True,
            "club": club.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["Club matching {id} not found"]
        }
    return payload

def listClubs_resolver(obj, info):
    try:
        clubs = [club.to_dict() for club in Club.query.all()]
        payload = {
            "success": True,
            "clubs": clubs
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
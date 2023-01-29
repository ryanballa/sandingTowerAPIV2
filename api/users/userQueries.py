from ..models import User
from ariadne import convert_kwargs_to_snake_case

@convert_kwargs_to_snake_case
def getUser_resolver(obj, info, id):
    def convertToInt(n):
        return int(n)
    
    try:
        user = User.query.get(id)
        payload = {
            "success": True,
            "user": user.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["User matching {id} not found"]
        }
    return payload

def listUsers_resolver(obj, info):
    try:
        users = [user.to_dict() for user in User.query.all()]
        payload = {
            "success": True,
            "users": users
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
from api import app, db
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType, format_error
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api import models
from api.users.userQueries import listUsers_resolver, getUser_resolver
from api.users.userMutations import create_user_resolver, update_user_resolver, delete_user_resolver
from api.clubs.clubQueries import listClubs_resolver, getClub_resolver
from api.clubs.clubMutations import create_club_resolver, update_club_resolver, delete_club_resolver

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listUsers", listUsers_resolver)
query.set_field("getUser", getUser_resolver)
query.set_field("listClubs", listClubs_resolver)
query.set_field("getClub", getClub_resolver)

mutation.set_field("createUser", create_user_resolver)
mutation.set_field("updateUser", update_user_resolver)
mutation.set_field("deleteUser", delete_user_resolver)

mutation.set_field("createClub", create_club_resolver)
mutation.set_field("updateClub", update_club_resolver)
mutation.set_field("deleteClub", delete_club_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

def format_errors(error, debug) -> dict:
    if app.debug:
        # If debug is enabled, reuse Ariadne's formatting logic (not required)
        return format_error(error, debug)

    # Create formatted error data
    formatted = error.formatted
    # Replace original error message with custom one
    formatted["message"] = "INTERNAL SERVER ERROR"
    return formatted

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug,
        validation_rules=[],
        error_formatter=format_errors
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code
from fastapi import APIRouter
import database
route = APIRouter()


@route.get("/users")
def get_users():

    return {"result": []}


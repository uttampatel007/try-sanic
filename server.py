import asyncio
from sqlalchemy import select
from pydantic import BaseModel, Field

from sanic import Sanic, Request, Websocket
from sanic.response import json
from sanic_ext import validate, openapi

from sanic.response import file_stream

from database import AsyncSessionLocal
from models import User


app = Sanic("TryApp")


app.config.HEALTH = True
app.config.HEALTH_ENDPOINT = True

# background task
async def auto_inject(app):
    await asyncio.sleep(5)
    print(app.name)


@app.route("/")
async def hello_world(request):

    app.add_task(auto_inject)

    async with AsyncSessionLocal() as session:
        # Insert a user into the database
        user = User(name="Uttam p")
        session.add(user)
        await session.commit()

        # Query the inserted user
        stmt = select(User).where(User.name == "Uttam P")
        result = await session.execute(stmt)
        user_query = result.scalar()

    return json({"message": "Hello, world.", "database_result": user_query.name if user_query else None})


@app.route("/name/<name>/")
async def get_name(request, name:str):
    return json({"name":name})


class UserProfile(BaseModel):
    name: str

@app.post("/user/")
@openapi.definition(
    body={
        "application/json": UserProfile.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
)
async def create_user(request):
    user = User(name=request.json["name"])
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return json({"user":user.name})


@app.get("/user/")
async def get_user(request):
    async with AsyncSessionLocal() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
    return json({"users": [user.name for user in users]})


@app.websocket('/feed')
async def foo3(request, ws):
    while True:
        data = await ws.recv()
        print('Received: ' + data)
        await ws.send(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


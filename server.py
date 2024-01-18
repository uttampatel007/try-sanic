import asyncio
from sqlalchemy import select

from sanic import Sanic, Request, Websocket
from sanic.response import json

from database import AsyncSessionLocal
from models import User


app = Sanic("TryApp")


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


@app.websocket('/feed')
async def foo3(request, ws):
    while True:
        data = await ws.recv()
        print('Received: ' + data)
        await ws.send(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


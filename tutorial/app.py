import asyncio
import itertools
import json
from connect4 import PLAYER1, PLAYER2, Connect4
import websockets
import secrets

async def handler(websocket):
    game = Connect4()
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)
    async for message in websocket:
        event = json.loads(message)
        assert event["signal"] == "start"
        msg = event["msg"]
        event = {
            "type": "chat",
            "player": player,
            "msg": msg,
        }
        await websocket.send(json.dumps(event))
        player = next(turns)
async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
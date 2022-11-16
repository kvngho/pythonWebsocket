# Websocket study

This pattern is so common that websockets provides a shortcut for iterating over messages received on the connection until the client disconnects:
```python
async def handler(websocket):
    async for message in websocket:
        print(message)
```


Before you exchange messages with the server, <b>you need to decide their format.</b> There is no universal convention for this.
In javascript:
```javascript
const websocket = new WebSocket("ws://localhost:8001/");
```
```javascript
const event = {type: "play", column: 3};
```
To send:
```javascript
websocket.send(JSON.stringify(event));
```

In JavaScript, you receive WebSocket messages by listening to message events. Here’s how to receive a message from the server and deserialize it from JSON:
```javascript
websocket.addEventListener("message", ({ data }) => {
  const event = JSON.parse(data);
  // do something with event
});
```

Sending an event from Python is quite similar to JavaScript:
```python
event = {"type": "play", "player": "red", "column": 3, "row": 0}
await websocket.send(json.dumps(event))
```

## Server Code

```python
import asyncio
import itertools
import json
from tutorial.connect4 import PLAYER1, PLAYER2, Connect4
import websockets


async def handler(websocket):
    game = Connect4()
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)
    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        try:
            row = game.play(player, column)
        except RuntimeError as exc:
            event = {
                "type": "error",
                "message": str(exc),
            }
            await websocket.send(json.dumps(event))
            continue
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))

        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner,
            }
            await websocket.send(json.dump(event))
        player = next(turns)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
```
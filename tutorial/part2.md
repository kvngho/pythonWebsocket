## Q. What if you need to scale to multiple server processes?
## A. In that case, you must design a way for the process that handles a given connection to be aware of relevant events for that client. This is often achieved with <b>a publish / subscribe mechanism.<b>

How can you make two connection handlers agree on which game they’re playing? When the first player starts a game, you give it an identifier. Then, you communicate the identifier to the second player. When the second player joins the game, you look it up with the identifier.

-> 첫번째 플레이어에서 identifier을 발급하고, 이걸로 두번째 플레이어와 소통

# 응용해서 채팅방을 만들어보자

# Chess
Chess UI created with tkinter and ChessBot trained with minimax with a depth of 4, supplemented with alpha-beta pruning.

First install the requirements with
```
pip install -r requirements.txt
```

To play against the bot, simply run
```
python main.py
```

To play on LAN,
first start a server with
```
python server_chess.py
```
then input your personal IP for the host and an unassigned port, such as 1234.
Then start your clients on any other devices in your LAN with
```
python client_chess.py
```
and input the IP address where the server is hosted, the assigned port, as well as the color of pieces ('w' for one 'b' for the other).

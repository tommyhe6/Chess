# Chess
Chess UI created with tkinter and ChessBot trained with minimax with a depth of 4, supplemented with alpha-beta pruning.

## Installation
To install the game, make sure you have tkinter installed, which you can do on MacOS with
```
brew install python-tk
```
or on Linux with
```
sudo apt-get install python3-tk
```
Install the required pyhton packaged with
```
pip install -r requirements.txt
```
## How to Play
Now that the software is installed, to play against the bot, simply run
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

## Future Improvements
- Handle all draw rules properly
- More robust engine with more modern AI/RL techniques to beat MuZero :)
- More appealing UI

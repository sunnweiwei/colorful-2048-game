# Colorful 2048 Game

A terminal-based implementation of the popular 2048 puzzle game with vibrant colors.

## Description

This is a Python implementation of the classic 2048 game that runs in your terminal. The game features:

- Colorful tiles that change based on their value
- Simple keyboard controls (W, A, S, D keys)
- Score tracking
- Clean and intuitive interface

## How to Play

1. Use the following keys to move the tiles:
   - W: Move Up
   - A: Move Left
   - S: Move Down
   - D: Move Right
   - Q: Quit Game

2. When two tiles with the same number touch, they merge into one tile with the sum of their values.

3. After each move, a new tile with a value of 2 (90% chance) or 4 (10% chance) appears in a random empty cell.

4. The goal is to create a tile with the value 2048.

## Requirements

- Python 3.6 or higher
- Colorama package

## Installation

1. Clone this repository:
```
git clone https://github.com/sunnweiwei/colorful-2048-game.git
cd colorful-2048-game
```

2. Install the required dependencies:
```
pip install colorama
```

3. Run the game:
```
python game.py
```

## Features

- Color-coded tiles for better visualization
- Score tracking
- Simple and intuitive controls
- Clean terminal interface

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the original 2048 game created by Gabriele Cirulli
- Built with Python and Colorama
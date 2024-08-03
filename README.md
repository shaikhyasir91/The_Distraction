# The Distraction Game

The Distraction Game is a fun and interactive game where the player navigates through various obstacles and enemies. The goal is to avoid distractions and reach the end of the level. This project also includes a level editor to create and customize game levels.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Level Editor](#level-editor)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features
- Player character with basic movement and jumping mechanics.
- Various types of enemies including Instagram, mobile, and football distractions.
- GIF animation when the player collides with a football enemy.
- Level editor to create and save custom levels.
- Load and save game levels using `pickle`.

## Installation
To run this game, you need to have Python and Pygame installed on your machine.

1. Clone the repository:
    ```bash
    git clone https://github.com/shaikhyasir91/The_Distraction.git
    ```

2. Install the required dependencies:
    ```bash
    pip install pygame
    ```

## Usage
### Running the Game
To run the main game, execute the `The Distraction.py` 
- script: [The Distraction.py](https://github.com/shaikhyasir91/The_Distraction/blob/3e16fe827eca3420753aff7169860dc7420860ab/The%20Distraction.py)


### Using the Level Editor
To create and edit game levels, execute the `level_editor.py` 
- script: [level_editor.py](https://github.com/shaikhyasir91/The_Distraction/blob/81b43d133b30d5f99af6e25e5fb7d670050485c1/level_editor.py)


## Level Editor
The level editor allows you to create custom levels for the game. You can place different types of tiles and enemies on the grid and save/load your level designs.

### Controls
- Left-click to place a tile or enemy.
- Right-click to remove a tile or enemy.
- Use the UP and DOWN arrow keys to change the level number.
- Press the Save button to save the current level.
- Press the Load button to load a saved level.

### Tile Types
- `0`: Empty
- `1`: Dirt Block
- `2`: Grass Block
- `3`: Football Enemy
- `4`: Horizontally Moving Platform
- `5`: Vertically Moving Platform
- `6`: Instagram Enemy
- `7`: Mobile Enemy
- `8`: Exit

## Screenshots
![Main Game](screenshots/main_game.png)
![Level Editor](screenshots/level_editor.png)

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

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
    git clone https://github.com/shaikhyasir91/TheDistractionGame.git
    cd TheDistractionGame
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install pygame
    ```

## Usage
### Running the Game
To run the main game, execute the `The Distraction.py` script:
```bash
python The Distraction.py

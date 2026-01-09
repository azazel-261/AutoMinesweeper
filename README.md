# AutoMinesweeper
This script is designed to play google's minesweeper game in the browser window. You can find it by simply typing "Minesweeper" in the google search box

## Setting up

### Install the requirements needed:

`pip install -r requirements.txt`

### Then, set up `config.ini` as follows: 

x and y variables count from the **top-left** corner of your monitor. You can use a graphics software like affinity to precisely determine the coordinates needed for your screen resolution and dpi

- `[WINDOW]` x and y should point to the top-left corner of the game window (the dark green stripe at the top that holds all the setting and info). Since it's only used to determine the presence of the game itself, precision is not required
- `[GAME]` x and y point to the top-left corner of **the mine field itself**. Please note that the script uses those to determine the pixel size of the field itself, so a mess-up here could make the program unreliable

### Run the script

#### Windows:

`python main.py`

MacOS/Linux:

`python3 main.py`

###### Note that neither i, nor this project are affiliated with Google in any way

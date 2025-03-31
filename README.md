### *Python version: 3.9*

### **The project was initially created on GitLab in December 2023 and later after little improvements transferred to GitHub without the commit history.*


## Project Goal: 
To create a program that allows playing the game Scrabble, developing a bot, preparing a GUI, and enabling game save and load functionalities.

## Project Description: 
The final version of the project enables playing Scrabble according to its rules (http://www.pfs.org.pl/reguly.php) and dictionary (https://sjp.pl/slownik/growy/) in a 1-on-1 match against a bot. The bot analyzes the board situation and can find the highest-scoring move (after a second), or choose to exchange tiles or pass. The player's view features a simple and clear GUI that prevents illegal moves. During gameplay, players can check rules, save, and load the game.

## User Instructions: 
To run the program, execute the screbble.py file. The game board appears on the left, the player's tile rack at the bottom right, and the rest of the interface above it. In the top right corner is the "About" button, toggling the game rules view (http://www.pfs.org.pl/reguly.php). To start a new game, press "New Game". Gameplay mostly follows the rules mentioned. Players use tiles from their rack to form words on the board, connecting with existing tiles. In their turn, players can place letters (click on a letter, then on the destination, and finally press "Put"), exchange any number of tiles (press "Exchange" and select unwanted tiles, then press the button again), or simply pass their turn (press "Pass"). The bot's turn follows immediately after the player's turn, which may take a moment. After the bot's turn, data is synchronized again, and it's the player's turn. The interface constantly displays player scores and newly formed words. The game ends when both players pass consecutively or when the letter bag and one player's rack run out of tiles. The final score is calculated based on the remaining tile values on the racks. If a player empties their rack, they receive additional points equal to the rack's value. Additionally, the dictionary can be modified by replacing the words.txt file and removing the words.trie file.

## Classes:
- Game (from the logic module): This class represents the game state created by the GUI through the "Load" or "New Game" button. Its attributes store all necessary game state data (enabling easy save and load) and the bot object. Its methods handle game mechanics, triggered by GUI signals, transforming attributes and returning new values.

- Ui_MainWindow (from the ui_scrabble module): Generated from a model created in the Designer program using PySide2-uic. This is the user interface project.

- ScrabbleWindow (from the gui module): GUI project inheriting from Ui_MainWindow. Besides inherited GUI elements, it holds the current game state (Game object) and the letter tile rack (QPushButton). Its methods include functional button actions for the interface and board positions. ScrabbleWindow sends signals to the logic part, synchronizing and presenting data in the interface.

- Bot: Stores and manages the word list in a Trie data structure (efficient for word finding). Its methods check words and decide the bot's move, the most demanding process in the project, utilizing multiprocessing for efficiency.

## Configuration/Text Files:
The project consists of the following files:

- Required: scrabble.py, in the game folder: gui.py, logic.py, ui_scrabble.py, bot.py, common_data.py, external_data.py, .env, and config/words.txt (dictionary input file).

- Optional but used (program can generate): save.json (data about the last saved game), words.trie (auxiliary file generated from words.txt, enhancing bot performance and word checking).

- Configuration: requirements.txt (environment setup).

- Tests: test_bot.py, test_common_data.py, test_external_data.py, test_logic.py.
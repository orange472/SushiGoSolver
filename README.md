# CPSC 474 Final Project | Sushi Go!

Sushi Go! is a multiplayer card game in which different cards combine for different amounts of points. The objective of the game is to score as many points as possible.

Each player receives a hand at the start of each round and selects one card to keep, passing the remaining cards to the player on their left. The chosen cards are revealed simultaneously after each round, impacting decisions in the next round. This process continues until there are no cards left.

The official rules can be found [here](https://gamewright.com/pdfs/Rules/SushiGoTM-RULES.pdf).

![Sushi Go!](https://cdn.thewirecutter.com/wp-content/media/2021/06/52-things-sushigo-2048px-5461-3x2-1.jpg?auto=webp&quality=75&crop=1.91:1&width=1200)
*An image of a standard Sushi Go! game.*

- [CPSC 474 Final Project | Sushi Go!](#cpsc-474-final-project--sushi-go)
  - [Description of Code](#description-of-code)
  - [Research Question](#research-question)
  - [Results](#results)

## Description of Code

- [sushi_go.py](sushi_go.py): Implements the SushiGo class, which initializes and simulates a game of Sushi Go! using the provided agents.
- [state.py](state.py): Implements a deck of cards and the SushiGoState class. The SushiGoState class contains information about each player's hands, as well as methods that calculate the current score and determine whether the current state is terminal.
- [agent.py](agent.py): An abstract base class for agents. Each agent requires a select_action method which returns an integer representing a card to select in a given round.
- [expectimax_agent.py](expectimax_agent.py): Implements an expectimax agent that can play against a predetermined agent or random strategy.
- [heuristic_agent.py](heuristic_agent.py): Implements a heuristic-based agent.
- [random_agent.py](random_agent.py): Implements a random choice agent.
- [test_sushi_go.py](test_sushi_go.py): Runs the implemented agents against each other (heuristic vs. random, expectimax vs. random, expectimax vs. heuristic).

To run the test script, run the makefile and then the following command:
```sh
./SushiGo --num_iterations=1000 --hand_size=6
```
Parameters:
- num_iterations: the number of games to run
- hand_size: the number of cards that each agent starts with

## Research Question

How well does a heuristic agent perform against a random agent? Then, how well does an expectimax agent perform against both the heuristic and random agent?

## Results

Over a period of 1000 games of hand size 6,
- Heuristic wins 74.45% of the time against random, with an average time of 7.23e-5 seconds per game.
- Expectimax with no early stopping wins 98.80% of the time against random, with an average time of 1.756 seconds per game, while expectimax *with* early stopping at a depth of 3 wins 96.95% of the time, with an average time of 0.179 seconds per game. 
- Expectimax (no early stopping) wins 97.15% of the time against heuristic, with an average time of 4.51e-3 seconds per game.
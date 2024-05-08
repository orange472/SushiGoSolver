import time
import argparse
from sushi_go import SushiGo
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
from expectimax_agent import ExpectimaxAgent

parser = argparse.ArgumentParser()
parser.add_argument("--num_iterations", type=int, default=100)
parser.add_argument("--hand_size", type=int, default=6)


# Function to run the test
def run_sushi_go_test():
    args = parser.parse_args()
    num_iters = args.num_iterations
    handsize = args.hand_size

    # Create instance of game
    game = SushiGo(handsize, logging=False)

    # Create instances of each agent (random, heuristic, expectimax)
    random_agent = RandomAgent()
    heuristic_agent = HeuristicAgent()
    expectimax_agent = ExpectimaxAgent()

    # Run heuristic agent against random agent
    print(
        f"P1 (\033[33mheuristic\033[0m) versus P2 (\033[33mrandom\033[0m) running over {num_iters} games of hand size {handsize}..."
    )
    start_time = time.time()
    game.run_agents(heuristic_agent, random_agent, num_iters)
    end_time = time.time()
    print(f"Time taken per trial: {(end_time - start_time) / num_iters} seconds")

    # Run expectimax agent against random agent
    print(
        f"P1 (\033[33mexpectimax\033[0m) versus P2 (\033[33mrandom\033[0m) running over {num_iters} games of hand size {handsize}..."
    )
    start_time = time.time()
    game.run_agents(expectimax_agent, random_agent, num_iters)
    end_time = time.time()
    print(f"Time taken per trial: {(end_time - start_time) / num_iters} seconds")

    # Run expectimax agent against heuristic agent
    print(
        f"P1 (\033[33mexpectimax\033[0m) versus P2 (\033[33mheuristic\033[0m) running over {num_iters} games of hand size {handsize}..."
    )
    start_time = time.time()
    expectimax_agent.opponent = heuristic_agent
    game.run_agents(expectimax_agent, heuristic_agent, num_iters)
    end_time = time.time()
    print(f"Time taken per trial: {(end_time - start_time) / num_iters} seconds")


# Run the test
run_sushi_go_test()

from agent import Agent
from state import Deck, SushiGoState


class SushiGo:
    def __init__(self, handsize=6, logging=False):
        self.handsize = handsize
        self.logging = logging
        self.deck = Deck()

    def run_agents(self, p1_agent: Agent, p2_agent: Agent, num_iters=1):
        p1_wins = 0
        p2_wins = 0

        for _ in range(num_iters):
            p1_state = self.deck.deal(self.handsize)

            while not p1_state.is_terminal():

                # p1_action = list of cards to move from hand to collection
                p1_action = p1_agent.select_action(p1_state)
                p2_state = p1_state.flip()
                p2_action = p2_agent.select_action(p2_state)

                opp_hand = list(p1_state.cur_hand)
                cur_collection = list(p1_state.cur_collection)

                if len(p1_action) == 2:
                    cur_collection.append(p1_action[0])
                    cur_collection.append(p1_action[1])
                    opp_hand.remove(p1_action[0])
                    opp_hand.remove(p1_action[1])
                    opp_hand.append(10)
                else:
                    cur_collection.append(p1_action[0])
                    if not p1_action[0] in opp_hand:
                        print(p1_action[0])
                    opp_hand.remove(p1_action[0])

                cur_hand = list(p2_state.cur_hand)
                opp_collection = list(p2_state.cur_collection)
                if len(p2_action) == 2:
                    opp_collection.append(p2_action[0])
                    opp_collection.append(p2_action[1])
                    cur_hand.remove(p2_action[0])
                    cur_hand.remove(p2_action[1])
                    cur_hand.append(10)
                else:
                    opp_collection.append(p2_action[0])
                    cur_hand.remove(p2_action[0])

                p1_state = SushiGoState(
                    cur_hand, opp_hand, cur_collection, opp_collection
                )

            p1_score, p2_score = p1_state.calculate_scores()

            if self.logging:
                print(p1_state)
                print(f"P1 score: {p1_score} | P2 score: {p2_score}")
                print("")

            if p1_score > p2_score:
                p1_wins += 1
            elif p1_score < p2_score:
                p2_wins += 1
            else:
                p1_wins += 0.5
                p2_wins += 0.5

        print(f"Average P1 wins: {p1_wins / num_iters}")
        print(f"Average P2 wins: {p2_wins / num_iters}")

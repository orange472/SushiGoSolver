from agent import Agent
from heuristic_agent import HeuristicAgent
from state import SushiGoState, card_names
from typing import Union, Dict, Tuple


class ExpectimaxAgent(Agent):
    def __init__(self, opponent: Union[Agent, None] = None):
        self.opponent = opponent
        self.dp: Dict[int, Tuple[int, int]] = {}

        self.heuristic = HeuristicAgent()
        self.max_depth = 6

    def select_action(self, state: SushiGoState):
        _, action = (
            self.search_against_random(state)
            if self.opponent is None
            else self.search_against_opponent(state)
        )

        return [action]

    def search_against_opponent(self, state: SushiGoState, depth=0) -> Tuple[int, int]:
        # Check cache for state
        key = hash(state)
        if key in self.dp:
            return self.dp[key]

        # Terminal state (base case)
        if state.is_terminal():
            p1_score, p2_score = state.calculate_scores()
            self.dp[key] = p1_score - p2_score, -1
            return p1_score - p2_score, -1

        # Initialize next state with opponent's chosen card
        opp_state = state.deep_flip()
        opp_card = self.opponent.select_action(opp_state)[0]
        opp_state.cur_collection.append(opp_card)
        opp_state.cur_hand.remove(opp_card)

        # Early stopping, play on using heuristic
        if depth >= 5:
            card = self.heuristic.select_action(state)[0]
            next_state = opp_state.deep_flip()
            next_state.cur_collection.append(card)
            next_state.cur_hand.remove(card)
            next_state.swap_hands()

            score, _ = self.search_against_opponent(next_state, depth + 1)
            return score, card

        # Also update next state with best response to opponent's action
        best_score = float("-infinity")
        best_card = -1

        for card in state.cur_hand:
            next_state = opp_state.deep_flip()
            next_state.cur_collection.append(card)
            next_state.cur_hand.remove(card)
            next_state.swap_hands()

            score, _ = self.search_against_opponent(next_state, depth + 1)
            if score > best_score:
                best_score = score
                best_card = card

        # Cache results
        self.dp[key] = best_score, best_card
        return best_score, best_card

    def search_against_random(self, state: SushiGoState, depth=0):
        # Check cache for state
        key = hash(state)
        if key in self.dp:
            return self.dp[key]

        if state.is_terminal():
            p1_score, p2_score = state.calculate_scores()
            score = 1 if p1_score > p2_score else -1 if p1_score < p2_score else 0
            return score, None

        # Early stopping, play on using heuristic
        if depth >= 3:
            card = self.heuristic.select_action(state)[0]
            opp_card = self.heuristic.select_action(state.flip())[0]
            state.cur_collection.append(card)
            state.cur_hand.remove(card)
            state.opp_collection.append(opp_card)
            state.opp_hand.remove(opp_card)
            state.swap_hands()

            score, _ = self.search_against_random(state, depth + 1)
            return score, card

        n = len(state.cur_hand)
        best_score: float = float("-infinity")
        best_card: int = -1

        for card in state.cur_hand:
            avg_score: float = 0

            for opp_card in state.opp_hand:
                # Update state
                next_state = state.deep_copy()
                next_state.cur_collection.append(card)
                next_state.cur_hand.remove(card)
                next_state.opp_collection.append(opp_card)
                next_state.opp_hand.remove(opp_card)
                next_state.swap_hands()

                # Run next search
                score, _ = self.search_against_random(next_state, depth + 1)
                avg_score += score

            # Update best score and best card
            avg_score = avg_score / n
            if avg_score > best_score:
                best_score = avg_score
                best_card = card

        # Cache results
        self.dp[key] = best_score, best_card
        return best_score, best_card

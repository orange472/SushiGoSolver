from state import SushiGoState
from agent import Agent
from state import card_names
from typing import List
import random

# card_names = [
#     "Tempura",  # 0
#     "Sashimi",  # 1
#     "Dumpling",  # 2
#     "Maki1",  # 3
#     "Maki2",  # 4
#     "Maki3",  # 5
#     "Salmon",  # 6
#     "Squid",  # 7
#     "Egg",  # 8
#     "Wasabi",  # 9
#     "Chopsticks",  # 10
# ]


class HeuristicAgent(Agent):
    def __init__(self):
        pass

    def get_cnts(self, sushi_go_list: List[int]):
        nigiri_cnt = 0
        wasabi_cnt = 0
        tempura_cnt = 0
        maki_cnt = 0
        dumpling_cnt = 0
        sashimi_cnt = 0
        for card in sushi_go_list:
            if card == 0:
                tempura_cnt += 1
            elif card == 1:
                sashimi_cnt += 1
            elif card == 2:
                dumpling_cnt += 1
            elif card == 3 or card == 4 or card == 5:
                maki_cnt += card - 2
            elif card == 6 or card == 7 or card == 8:
                nigiri_cnt += 1
            elif card == 9:
                wasabi_cnt += 1
        return nigiri_cnt, wasabi_cnt, tempura_cnt, maki_cnt, dumpling_cnt, sashimi_cnt

    def select_action(self, state: SushiGoState):
        cur_round = len(state.cur_collection) + 1

        card_counts = [0] * len(card_names)
        for card in state.cur_hand:
            card_counts[card] += 1

        card_values = [0] * len(card_names)

        cur_hand_cnts = self.get_cnts(state.cur_hand)
        opp_hand_cnts = self.get_cnts(state.opp_hand)
        cur_collection_cnts = self.get_cnts(state.cur_collection)
        opp_collection_cnts = self.get_cnts(state.opp_collection)

        # Check if we have wasabi
        has_wasabi = cur_collection_cnts[0] < cur_collection_cnts[1]

        # Calculate ~EV of nigiri
        if has_wasabi:
            card_values[6] += 6
            card_values[7] += 9
            card_values[8] += 3
        else:
            card_values[6] += 2
            card_values[7] += 3
            card_values[8] += 1

        # Calculate ~EV of tempura
        if cur_round > 1:
            if cur_collection_cnts[2] % 2 == 1:
                card_values[0] += 5
            elif opp_collection_cnts[2] % 2 == 1 and (
                opp_hand_cnts[2] == 0 and cur_hand_cnts[2] == 1
            ):
                card_values[0] += 5
            elif (cur_round < 4) and (cur_hand_cnts[2] + opp_hand_cnts[2] > 1):
                card_values[0] += 2.5 / (
                    4 - min(3, cur_hand_cnts[2] + opp_hand_cnts[2])
                )
            else:
                card_values[0] += 0.1

        # Calculate ~EV of sashimi (only check for blocking)
        if cur_round > 1:
            if opp_collection_cnts[5] % 3 == 2 and (
                opp_hand_cnts[5] == 0 and cur_hand_cnts[5] == 1
            ):
                card_values[1] += 10

        # Calculate ~EV of wasabi
        if not has_wasabi:
            if cur_round < 5:
                if opp_hand_cnts[0] > 1:
                    card_values[9] += 2.5

        # Calculate ~EV of dumplings
        card_values[2] += 1 + cur_collection_cnts[4]
        if cur_round > 1:
            if cur_round < 4:
                card_values[2] += (cur_hand_cnts[4] + opp_hand_cnts[4]) * 0.1

        # Calculate ~EV of maki
        if cur_round > 1:
            total_maki_left = cur_hand_cnts[3] + opp_hand_cnts[3]
            if cur_collection_cnts[3] <= opp_collection_cnts[3] + total_maki_left:
                if (
                    cur_collection_cnts[3] + 1
                    > opp_collection_cnts[3] + total_maki_left - 1
                ):
                    card_values[3] += 3
                    card_values[4] += 3
                    card_values[5] += 3
                elif (
                    cur_collection_cnts[3] + 2
                    > opp_collection_cnts[3] + total_maki_left - 2
                ):
                    card_values[4] += 3
                    card_values[5] += 3
                elif (
                    cur_collection_cnts[3] + 3
                    > opp_collection_cnts[3] + total_maki_left - 3
                ):
                    card_values[5] += 3
                elif cur_collection_cnts[3] + 1 > opp_collection_cnts[3]:
                    card_values[3] += 0.15
                    card_values[4] += 0.6
                    card_values[5] += 1.35
                elif cur_collection_cnts[3] + 2 > opp_collection_cnts[3]:
                    card_values[4] += 0.15
                    card_values[5] += 0.6
                elif cur_collection_cnts[3] + 3 > opp_collection_cnts[3]:
                    card_values[5] += 0.15
        else:
            card_values[3] += 0.15
            card_values[4] += 0.6
            card_values[5] += 1.35

        sorted_card_values = sorted(
            enumerate(card_values), key=lambda x: x[1], reverse=True
        )
        for card, _ in sorted_card_values:
            if card_counts[card] > 0:
                return [card]

        return [random.choice(state.cur_hand)]

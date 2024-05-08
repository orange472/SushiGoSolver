from typing import List
import random

card_names = [
    "Tempura 🍤",  # 0
    "Sashimi 🍣",  # 1
    "Dumpling 🥟",  # 2
    "Maki1 🥬",  # 3
    "Maki2 🥬",  # 4
    "Maki3 🥬",  # 5
    "Salmon 🐟",  # 6
    "Squid 🦑",  # 7
    "Egg 🍳",  # 8
    "Wasabi 🥑",  # 9
    "Chopsticks 🥢",  # 10
]

card_counts = [14, 14, 14, 6, 12, 8, 10, 5, 5, 6, 4]


class Deck:
    def __init__(self):
        self.deck: List[int] = []

        for i, count in enumerate(card_counts):
            self.deck.extend([i] * count)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, n: int):
        self.shuffle()
        cur_hand = self.deck[:n]
        opp_hand = self.deck[n : (2 * n)]
        return SushiGoState(cur_hand, opp_hand, [], [])


class SushiGoState:
    def __init__(
        self,
        cur_hand: List[int],
        opp_hand: List[int],
        cur_collection: List[int],
        opp_collection: List[int],
    ):
        self.cur_hand = cur_hand
        self.opp_hand = opp_hand

        self.cur_collection = cur_collection
        self.opp_collection = opp_collection

    def __str__(self):
        prompt = "P1 Hand: "
        if len(self.cur_hand) == 0:
            prompt += "Empty"
        for card in self.cur_hand:
            prompt += card_names[card] + " "
        prompt += "\n"

        prompt += "P1 Collection: "
        if len(self.cur_collection) == 0:
            prompt += "Empty"
        for card in self.cur_collection:
            prompt += card_names[card] + " "
        prompt += "\n"

        prompt += "P2 Hand: "
        if len(self.opp_hand) == 0:
            prompt += "Empty"
        for card in self.opp_hand:
            prompt += card_names[card] + " "
        prompt += "\n"

        prompt += "P2 Collection: "
        if len(self.opp_collection) == 0:
            prompt += "Empty"
        for card in self.opp_collection:
            prompt += card_names[card] + " "

        return prompt

    def __hash__(self):
        # Convert lists to tuples for hashing
        tuple1 = tuple(self.cur_hand)
        tuple2 = tuple(self.opp_hand)
        tuple3 = tuple(self.cur_collection)
        tuple4 = tuple(self.opp_collection)

        # Combine all tuples into one tuple and hash it
        return hash((tuple1, tuple2, tuple3, tuple4))

    def deep_copy(self):
        return SushiGoState(
            cur_hand=self.cur_hand.copy(),
            opp_hand=self.opp_hand.copy(),
            cur_collection=self.cur_collection.copy(),
            opp_collection=self.opp_collection.copy(),
        )

    def is_terminal(self):
        return (len(self.cur_hand) == 0) and (len(self.opp_hand) == 0)

    def calculate_scores(self):
        p1_score, p1_maki_count = self._calculate_score_without_maki(
            self.cur_collection
        )
        p2_score, p2_maki_count = self._calculate_score_without_maki(
            self.opp_collection
        )

        if p1_maki_count > p2_maki_count:
            p1_score += 6
        elif p1_maki_count < p2_maki_count:
            p2_score += 6
        else:
            p1_score += 3
            p2_score += 3

        return p1_score, p2_score

    def deep_flip(self):
        return SushiGoState(
            cur_hand=self.opp_hand.copy(),
            opp_hand=self.cur_hand.copy(),
            cur_collection=self.opp_collection.copy(),
            opp_collection=self.cur_collection.copy(),
        )

    def flip(self):
        return SushiGoState(
            cur_hand=self.opp_hand,
            opp_hand=self.cur_hand,
            cur_collection=self.opp_collection,
            opp_collection=self.cur_collection,
        )

    def swap_hands(self):
        temp = self.cur_hand
        self.cur_hand = self.opp_hand
        self.opp_hand = temp

    def _calculate_score_without_maki(self, collection: List[int]):
        maki_count: int = 0
        wasabi_count: int = 0
        tempura_count: int = 0
        sashimi_count: int = 0
        dumpling_count: int = 0
        score: int = 0

        for card in collection:
            # Tempura
            if card == 0:
                tempura_count += 1
            # Sashimi
            elif card == 1:
                sashimi_count += 1
            # Dumpling
            elif card == 2:
                dumpling_count += 1
            # Maki roll, count 1
            elif card == 3:
                maki_count += 1
            # Maki roll, count 2
            elif card == 4:
                maki_count += 2
            # Maki roll, count 3
            elif card == 5:
                maki_count += 3
            # Wasabi
            elif card == 9:
                wasabi_count += 1
            # At this point, card must be Nigiri
            elif wasabi_count > 0:
                score += 9 if card == 7 else 6 if card == 6 else 3
                wasabi_count -= 1
            else:
                score += 3 if card == 7 else 2 if card == 6 else 1

            if tempura_count == 2:
                score += 5
                tempura_count = 0

            if sashimi_count == 3:
                score += 10
                sashimi_count = 0

        if dumpling_count >= 5:
            score += 15
        elif dumpling_count == 4:
            score += 10
        elif dumpling_count == 3:
            score += 6
        elif dumpling_count == 2:
            score += 3
        elif dumpling_count == 1:
            score += 1

        return score, maki_count

"""
Cribbage hand scoring calculator.
"""

from itertools import combinations


RANK_VALUES = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10,
}

RANK_ORDER = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
}


def _parse_card(card_str):
    rank = card_str[0]
    suit = card_str[1]
    return (rank, suit)


def _count_fifteens(cards):
    """Count all subsets of cards whose values sum to 15. Each scores 2."""
    values = [RANK_VALUES[r] for r, s in cards]
    count = 0
    for size in range(2, len(values) + 1):
        for combo in combinations(values, size):
            if sum(combo) == 15:
                count += 1
    return count * 2


def _count_pairs(cards):
    """Count all pairs of cards with the same rank. Each pair scores 2."""
    ranks = [r for r, s in cards]
    count = 0
    for i in range(len(ranks)):
        for j in range(i + 1, len(ranks)):
            if ranks[i] == ranks[j]:
                count += 1
    return count * 2


def _count_runs(cards):
    """Count runs of 3+ consecutive ranks, multiplied by duplicates."""
    ranks = [RANK_ORDER[r] for r, s in cards]
    freq = {}
    for r in ranks:
        freq[r] = freq.get(r, 0) + 1

    sorted_unique = sorted(freq.keys())

    # Find all maximal consecutive sequences
    sequences = []
    current_seq = [sorted_unique[0]]
    for i in range(1, len(sorted_unique)):
        if sorted_unique[i] == sorted_unique[i - 1] + 1:
            current_seq.append(sorted_unique[i])
        else:
            sequences.append(current_seq)
            current_seq = [sorted_unique[i]]
    sequences.append(current_seq)

    score = 0
    for seq in sequences:
        if len(seq) >= 3:
            multiplier = 1
            for r in seq:
                multiplier *= freq[r]
            score += len(seq) * multiplier

    return score


def _count_flush(hand_cards, starter_card, is_crib):
    """Count flush points."""
    hand_suits = [s for r, s in hand_cards]
    if len(set(hand_suits)) != 1:
        return 0

    if is_crib:
        # Crib requires all 5 cards same suit
        if starter_card[1] == hand_suits[0]:
            return 5
        return 0
    else:
        # Regular hand: 4 hand cards same suit = 4, +1 if starter matches
        if starter_card[1] == hand_suits[0]:
            return 5
        return 4


def _count_nobs(hand_cards, starter_card):
    """Check if hand contains the Jack of the starter's suit."""
    starter_suit = starter_card[1]
    for rank, suit in hand_cards:
        if rank == 'J' and suit == starter_suit:
            return 1
    return 0


def score_hand(hand, starter, is_crib=False):
    """
    Score a cribbage hand.

    Args:
        hand: list of 4 card strings (e.g., ["5H", "5D", "5S", "JC"])
        starter: single card string (e.g., "5C")
        is_crib: bool, if True use crib flush rules (default False)

    Returns:
        dict with keys "fifteens", "pairs", "runs", "flush", "nobs", "total"
    """
    hand_cards = [_parse_card(c) for c in hand]
    starter_card = _parse_card(starter)
    all_cards = hand_cards + [starter_card]

    fifteens = _count_fifteens(all_cards)
    pairs = _count_pairs(all_cards)
    runs = _count_runs(all_cards)
    flush = _count_flush(hand_cards, starter_card, is_crib)
    nobs = _count_nobs(hand_cards, starter_card)

    return {
        "fifteens": fifteens,
        "pairs": pairs,
        "runs": runs,
        "flush": flush,
        "nobs": nobs,
        "total": fifteens + pairs + runs + flush + nobs,
    }

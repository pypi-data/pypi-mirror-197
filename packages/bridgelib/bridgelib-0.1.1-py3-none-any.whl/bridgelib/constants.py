# declare constants

PLAYERS = ['N', 'E', 'S', 'W']
PLAYERS_COUNT = len(PLAYERS)

CARD_COLORS = ['s', 'h', 'd', 'c']
CARD_VALUES = ['A', 'K', 'Q', 'J', 'T'] + [str(x) for x in range(9,1,-1)]
ALL_CARDS_COUNT = len(CARD_COLORS) * len(CARD_VALUES)

HAND_CARDS_COUNT = ALL_CARDS_COUNT / PLAYERS_COUNT

BID_COLORS = ['c', 'd', 'h', 's', 'nt']
BID_VALUES = [str(x) for x in range(1, 8)]
SPECIAL_BIDS = ["pass", "dbl", "rdbl"]
ALL_BIDS_COUNT = len(BID_COLORS) * len(BID_VALUES) + len(SPECIAL_BIDS)

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from random import shuffle
import json


class CardKind(Enum):
    ROLE = auto()
    PANIC = auto()
    ACTION = auto()
    DEFENSE = auto()
    OBSTACLE = auto()


class CardType(str, Enum):
    THE_THING = "The Thing"
    INFECTED = "Infected"
    FLAMETHROWER = "Flamethrower"
    ANALYSIS = "Analysis"
    AXE = "Axe"
    SUSPICIOUS = "Suspicious"
    WHISKEY = "Whiskey"
    RESOLUTE = "Resolute"
    WATCH_YOUR_BACK = "Watch Your Back"
    CHANGE_PLACES = "Change Places"
    YOUD_BETTER_RUN = "You'd Better Run"
    SEDUCTION = "Seduction"
    SCARY = "Scary"
    IM_COMFORTABLE = "I'm Comfortable"
    NO_THANKS = "No Thanks"
    MISSED = "Missed"
    NO_BARBECUE = "No Barbecue"
    QUARANTINE = "Quarantine"
    BARRED_DOOR = "Barred Door"
    ROTTEN_ROPES = "Rotten Ropes"
    ONE_TWO_THREE = "One Two Three"
    FOUR_FIVE_SIX = "Four Five Six"
    WHERES_THE_PARTY = "Wheres The Party"
    GET_OUT_OF_HERE = "Get Out Of Here"
    FORGETFUL = "Forgetful"
    RING_AROUND_THE_ROSIE = "Ring Around The Rosie"
    LETS_BE_FRIENDS = "Lets Be Friends"
    BLIND_DATE = "Blind Date"
    OOOPS = "Ooops"
    BETWEEN_US = "Between Us"
    REVELATIONS = "Revelations"


@dataclass(eq=True, frozen=True)
class Card:
    card_type: CardType

    @property
    def kind(self) -> CardKind:
        match self.card_type:
            case CardType.THE_THING | CardType.INFECTED:
                return CardKind.ROLE
            case (
                CardType.FLAMETHROWER
                | CardType.ANALYSIS
                | CardType.AXE
                | CardType.SUSPICIOUS
                | CardType.WHISKEY
                | CardType.RESOLUTE
                | CardType.WATCH_YOUR_BACK
                | CardType.CHANGE_PLACES
                | CardType.YOUD_BETTER_RUN
                | CardType.SEDUCTION
            ):
                return CardKind.ACTION
            case (
                CardType.SCARY
                | CardType.IM_COMFORTABLE
                | CardType.NO_THANKS
                | CardType.MISSED
                | CardType.NO_BARBECUE
            ):
                return CardKind.DEFENSE
            case CardType.QUARANTINE | CardType.BARRED_DOOR:
                return CardKind.OBSTACLE
            case (
                CardType.ROTTEN_ROPES
                | CardType.ONE_TWO_THREE
                | CardType.FOUR_FIVE_SIX
                | CardType.WHERES_THE_PARTY
                | CardType.GET_OUT_OF_HERE
                | CardType.FORGETFUL
                | CardType.RING_AROUND_THE_ROSIE
                | CardType.LETS_BE_FRIENDS
                | CardType.BLIND_DATE
                | CardType.OOOPS
                | CardType.BETWEEN_US
                | CardType.REVELATIONS
            ):
                return CardKind.PANIC

    @property
    def terminates(self) -> bool:
        return False  # TODO

    @property
    def description(self) -> str:
        match self.card_type:
            case CardType.THE_THING:
                return "You are the thing"
            case CardType.INFECTED:
                return "If you receive this card from another player, you become infected and cannot discard it again until the end of the game"
            case CardType.FLAMETHROWER:
                return "Choose an adjacent player and eliminate them from the game"
            case CardType.ANALYSIS:
                return "Force an adjacent player to show you all their cards"
            case CardType.AXE:
                return "Remove a 'Barred Door' or 'Quarentine' card played on yourself or an adjacent player"
            case CardType.SUSPICIOUS:
                return "Look at a random card from an adjacent player's hand"
            case CardType.WHISKEY:
                return "Show all cards to all other players. You can only play this on yourself"
            case CardType.RESOLUTE:
                return "Draw three 'Stay Away!' cards, choose one and discard the others, then play or discard a card"
            case CardType.WATCH_YOUR_BACK:
                return "Reverse the turn order. From now on both the game and card exchange will take place in the opposite direction"
            case CardType.CHANGE_PLACES:
                return "Swap places with an adjacent player who is not in Quarantine or behind a Barred Door"
            case CardType.YOUD_BETTER_RUN:
                return "Swap places with a player of your choice who is not in Quarantine. This ignores Barred Doors"
            case CardType.SEDUCTION:
                return "Trade a card with any player who is not in quarentine. Your turn ends"
            case CardType.SCARY:
                return "Decline a card exchange and view the rejected card. Draw a 'Stay Away' card replacement"
            case CardType.IM_COMFORTABLE:
                return "Refuse a 'Steal the Place' or a 'Knock it off!'. Draw a 'Stay Away' card replacement"
            case CardType.NO_THANKS:
                return "Decline a card exchange. Draw a 'Stay Away' card replacement"
            case CardType.MISSED:
                return "The next player makes the card exchange for you. If they recieve an 'Infected!', they will not become infected. Draw a 'Stay Away!' card replacement"
            case CardType.NO_BARBECUE:
                return "Nullifies the effect if a Flamethrower played on you. Draw a 'Stay Away!' card replacement"
            case CardType.QUARANTINE:
                return "For 2 turns an adjacent player draws, discards and exchanges cards face up. They cannot eliminate players or move"
            case CardType.BARRED_DOOR:
                return "Place this card between you and an adjacent player. No more action is allowed between you"
            case CardType.ROTTEN_ROPES:
                return "Those old ropes you used are so easy to break! All Quarantine cards in play are removed and discarded"
            case CardType.ONE_TWO_THREE:
                return "...the Thing comes looking for you! You can choose to switch places with the 3rd player to your right or left, ignoring any Barred Door cards in play. If one of you is in Quarantine, the exchange to does not take place"
            case CardType.FOUR_FIVE_SIX:
                return "You are not safe! All Barred Door cards in play are removed and discarded"
            case CardType.WHERES_THE_PARTY:
                return "Remove all 'Quarantine' and 'Barred Door' cards in play. Starting with you and proceeding clockwise, all players trade places. In cases of odd players the last on does not move"
            case CardType.GET_OUT_OF_HERE:
                return "Swap places with a player of your choice. If either of you is in Quarantine the exchange will not occur"
            case CardType.FORGETFUL:
                return "Discard three cards from your hand and draw three more 'Stay Away!' cards, discarding the 'Panic!' cards discovered in this way"
            case CardType.RING_AROUND_THE_ROSIE:
                return "At the same time, each player passes a card to the next player, following the direction of game, ignoring any Barred Door or Quarantine cards in play. You cannot use any card to cancel this exchange. The Thing can infect by passing an 'Infected!' card in this way. Your turn ends"
            case CardType.LETS_BE_FRIENDS:
                return (
                    "Trade a card with a player of your choice who is not in Quarantine"
                )
            case CardType.BLIND_DATE:
                return "Swap a card from your hand with the top of the deck, discarding the 'Panic' discovered in this way. Your turn ends"
            case CardType.OOOPS:
                return "Show your cards to all players"
            case CardType.BETWEEN_US:
                return "Show your cards to an adjacent player of your choice"
            case CardType.REVELATIONS:
                return "Starting with you and following the direction of the game, everyone chooses whether or not to reveal their hand. The 'Revelations' round end if a player shows an 'Infected!' card"


class Deck:
    _cards: list[Card]

    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards

    @property
    def size(self) -> int:
        return len(self._cards)

    @property
    def top_card_kind(self) -> Optional[CardKind]:
        return None if self.size == 0 else self._cards[0].kind

    def draw(self) -> Optional[Card]:
        """Draw a card from the deck"""
        if self.size == 0:
            return None
        return self._cards.pop(0)

    def get_the_thing(self) -> Optional[Card]:
        for idx, card in enumerate(self._cards):
            if card.card_type == CardType.THE_THING:
                return self._cards.pop(idx)

        return None

    def get_deal_card(self) -> Optional[Card]:
        for idx, card in enumerate(self._cards):
            if card.kind != CardKind.PANIC and card.kind != CardKind.ROLE:
                return self._cards.pop(idx)
        return None

    def add_card(self, card: Card) -> None:
        """Add a card to the deck"""
        self._cards.append(card)

    def shuffle(self) -> None:
        """Shuffle the deck"""
        shuffle(self._cards)


class DeckFactory:
    _config: Optional[dict[str, dict[str, int]]] = None
    CONFIG_FILE = "card_counts.json"

    @staticmethod
    def create_deck(player_count: int) -> Deck:
        """Creates a deck based on the player count"""
        assert 4 <= player_count <= 12

        if DeckFactory._config is None:
            DeckFactory._load_config()

        deck_description = DeckFactory._config.get(str(player_count))
        cards: list[Card] = []

        for card_name, card_count in deck_description.items():
            for _ in range(card_count):
                cards.append(CardFactory.create_card(card_name))

        return Deck(cards)

    @staticmethod
    def _load_config():
        """Reads the config file and stores it in `_config`"""
        with open(DeckFactory.CONFIG_FILE) as config_file:
            DeckFactory._config = json.load(config_file)


class CardFactory:
    @staticmethod
    def create_card(name: str) -> Card:
        return Card(name)

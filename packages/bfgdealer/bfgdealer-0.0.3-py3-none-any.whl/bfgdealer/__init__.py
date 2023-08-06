"""Expose the classes in the API."""

from ._version import __version__
VERSION = __version__

from .source.board import Board, Trick, Contract, Auction
from .source.dealer import Dealer
from .source.dealer_solo import Dealer as DealerSolo, SET_HANDS as SOLO_SET_HANDS
from .source.dealer_duo import Dealer as DealerDuo, SET_HANDS as DUO_SET_HANDS
from .source.dealer_engine import DealerEngine

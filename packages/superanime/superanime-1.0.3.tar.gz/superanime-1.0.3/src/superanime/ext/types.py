from enum import Enum, EnumMeta
from typing import Any

class EnumeratorMeta(EnumMeta):
    def __contains__(cls, member: Any):
        if type(member) == cls:
            return EnumMeta.__contains__(cls, member)
        else:
            try:
                cls(member)
            except ValueError:
                return False
            return True

    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value
        return value
        
class Enumerator(Enum, metaclass=EnumeratorMeta):
    pass

class SFWGif(Enumerator):
    """
    SFW ANIME GIFs Types
    """
    ANGRY: str = "angry"
    BAKA: str = "baka"
    BITE: str = "bite"
    BLUSH: str = "blush"
    CRY: str = "cry"
    DANCE: str = "dance"
    DEREDERE: str = "deredere"
    HAPPY: str = "happy"
    HUG: str = "hug"
    KISS: str = "kiss"
    PAT: str = "pat"
    PUNCH: str = "punch"
    SLAP: str = "slap"
    SLEEP: str = "sleep"
    SMUG: str = "smug"


class NSFWGif(Enumerator):
    """
    NSFW ANIME GIFs Types
    """
    ANAL: str = "anal"
    FUCK: str = "fuck"
    SUCK: str = "suck"

class SearchType(Enumerator):
    """
    Manga or Anime
    """
    ANIME: str = "anime"
    MANGA: str = "manga"

from ..superanime.ext import utils
from ..superanime.ext.types import SFWGif, NSFWGif, SearchType
from ..superanime.ext.objects import GifResult, Titles, SearchResult
 
from typing import Optional
import random, json
from pystyle import Colors, Colorate

 
class AnimeClient:
    def __init__(self, *, print_on_ready: bool = True, cache_on_startup: bool = True) -> None:
        self.print_on_ready = print_on_ready
        self.cache = {}

    def __read_json(self, x) -> dict:   
        return json.loads(x.decode('utf8'))
        
    async def __load_gifs(self) -> None:
        _d = { "sfw": {}, "nsfw": {} }
        for _ in SFWGif:
            _d["sfw"][_.value] = self.__read_json(await utils.Request(
                url=f"https://raw.githubusercontent.com/MoonlightGroup/superanime.db/main/sfw/{_.value}.json",
                like="read"
            ))
        for _ in NSFWGif:
            _d["nsfw"][_.value] = self.__read_json(await utils.Request(
                url=f"https://raw.githubusercontent.com/MoonlightGroup/superanime.db/main/nsfw/{_.value}.json",
                like="read"
            ))
        
        self.cache = _d

    async def start(self) -> None:
        await self.__load_gifs()
        if self.print_on_ready:
            print("\n   Started", Colorate.Horizontal(Colors.rainbow, 'SuperAnime.py'), '\n')
        
    def gif(self, bucket: SFWGif | str | NSFWGif, *, as_object: Optional[bool] = True) -> GifResult | str:
        _res = None
        if bucket in SFWGif:
            _res = self.cache["sfw"][bucket]
        elif bucket in NSFWGif:
            _res = self.cache["nsfw"][str(bucket)]
        else:
            raise ValueError("The provided gif cannot be found in SuperAnime")
        if not _res:
            raise ValueError("The provided gif cannot be found in SuperAnime")

        _ = random.choice(_res)
        return GifResult(
            url=_["url"],
            title=Titles(**_["title"]),
            episode=_["episode"]
        ) if as_object else _["url"]

    async def search(self, query: str, *, type: str | SearchType = None):
        data = None
        try:
            if not type:
                data = await utils.Request(
                    url=f"https://kitsu.io/api/edge/anime?filter[text]={query.strip()}&page[offset]=0"
                )
            else:
                if isinstance(type, SearchType):
                    data = (await utils.Request(
                        url=f"https://kitsu.io/api/edge/{type.value.lower()}?filter[text]={query.strip()}&page[offset]=0"
                    ))
                elif isinstance(type, str):
                    if type in SearchType:
                        data = (await utils.Request(
                            url=f"https://kitsu.io/api/edge/{type.lower().strip()}?filter[text]={query.strip()}&page[offset]=0"
                        ))
        except:
            raise utils.SearchError("An error occurred when searching for the anime or manga, try to check if the query is correct.")
        if not data["data"]: 
            raise utils.SearchError("The anime or manga could not be found, try to check if the query is correct.")
        
        return data["data"]


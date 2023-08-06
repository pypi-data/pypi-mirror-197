from ..ext import utils, types as TS 
import typing, random, json, pkg_resources


async def AnimeSearch(*, query: str, type = None):
    data = None
    try:
        if not type:
            data = await utils.Request(
                url=f"https://kitsu.io/api/edge/anime?filter[text]={query.strip()}&page[offset]=0"
            )
        else:
            if isinstance(type, TS.SearchType):
                data = (await utils.Request(
                    url=f"https://kitsu.io/api/edge/{type.value.lower()}?filter[text]={query.strip()}&page[offset]=0"
                ))
            elif isinstance(type, str):
                if type in TS.SearchType:
                    data = (await utils.Request(
                        url=f"https://kitsu.io/api/edge/{type.lower().strip()}?filter[text]={query.strip()}&page[offset]=0"
                    ))
    except:
        raise utils.SearchError("An error occurred when searching for the anime or manga, try to check if the query is correct.")
    if not data["data"]: 
        raise utils.SearchError("The anime or manga could not be found, try to check if the query is correct.")
        
    return data["data"]
       
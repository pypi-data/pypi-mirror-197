from superanime.utils import Request
import superanime.types as TS
import typing, random, json, pkg_resources

class SearchError(Exception):
    pass

class InvalidGifType(Exception):
    pass

def AnimeGif(*, bucket: str, as_dict: typing.Optional[bool] = True):
    path, dir = None, lambda x, y: pkg_resources.resource_filename('superanime', f"anime/gifs/{x}/{y}.json")
    if isinstance(bucket, TS.NsfwGif):
        path = dir('sfw', bucket.value)
    elif isinstance(bucket, TS.SfwGif):
        path = dir('sfw', bucket.value)
    elif isinstance(bucket, str):
        if bucket in TS.SfwGif:
           path = dir('sfw', bucket)
        if bucket in TS.NsfwGif:
           path = dir('nsfw', bucket)
    else:
        raise InvalidGifType("The provided gif cannot be found in Anime.py")
    if not path:
        raise InvalidGifType("The provided gif cannot be found in Anime.py")
    
    with open(path) as Data:
        data = json.load(Data)
    return random.choice(data) if as_dict else random.choice(data)["url"]

async def AnimeSearch(*, query: str, type = None):
    data = None
    try:
        if not type:
            data = await Request(
                url=f"https://kitsu.io/api/edge/anime?filter[text]={query.strip()}&page[offset]=0"
            )
        else:
            if isinstance(type, TS.SearchType):
                data = (await Request(
                    url=f"https://kitsu.io/api/edge/{type.value.lower()}?filter[text]={query.strip()}&page[offset]=0"
                ))
            elif isinstance(type, str):
                if type in TS.SearchType:
                    data = (await Request(
                        url=f"https://kitsu.io/api/edge/{type.lower().strip()}?filter[text]={query.strip()}&page[offset]=0"
                    ))
    except:
        raise SearchError("An error occurred when searching for the anime or manga, try to check if the query is correct.")
    if not data["data"]: 
        raise SearchError("The anime or manga could not be found, try to check if the query is correct.")
        
    return data["data"]
       
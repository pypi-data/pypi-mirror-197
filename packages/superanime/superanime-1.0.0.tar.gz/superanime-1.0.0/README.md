# SuperAnime
The best package in Python to get anime information and anime gifs!

## Installation:
```
pip install superanime
```

## Example Usage:
```py
import asyncio

from superanime import AnimeClient
from superanime.ext.types import SFWGif, SearchType

anime = AnimeClient() 

async def main():
    await anime.start() # Starts the client
    
    gif = anime.gif(
        bucket=SFWGif.KISS, # Also works with strings!
        as_object=True # If you want to send a 'GifResult' object with additional info like anime name. Default to 'True'
    )
    print(gif.url) # Print the GIF URL

    search = await anime.search(
        query="One Piece", # The query to search in kitsu.io
        type=SearchType.ANIME # The type of search you want to search for. ('ANIME' or 'MANGA') If none provided the anime type will be searched.
    )
    print(search.name) # Print the Anime name
    
if __name__ == "main":
    asyncio.run(main())
```


## Methods:

```py
superanime.AnimeClient(print_on_ready: bool = True) -> AnimeClient

AnimeClient.gif(bucket: SFWGif | NSFWGif | str, as_object: bool = True) -> GifResult
Anime.search(query: str, type: SearchType | str = None) -> SearchResult
```
<br/>
    
   _~ Made by Noraa08 for MoonlightGroup_
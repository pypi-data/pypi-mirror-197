from dataclasses import dataclass

@dataclass
class Titles:
    native: str
    romaji: str
    english: str

@dataclass
class GifResult:
    """
    Object representation of an anime gif result
    """
    url: str
    title: Titles
    episode: int

@dataclass
class ImageCover:
    tiny: str
    small: str
    medium: str
    large: str
    original: str

@dataclass
class SearchAttributes:
    created_at: str
    updated_at: str
    synopsis: str
    description: str
    titles: Titles
    canonical_title: str
    avarage_rating: str
    user_count: int
    favorites_count: int
    start_date: str
    end_date: str
    next_relase: str
    popularity_ranking: str
    rating_rank: int
    age_rating: str
    cover_image: ImageCover
    poster_image: ImageCover
    
@dataclass
class SearchResult:
    """
    Object representation of an anime search rsult 
    """
    id: int
    type: str
    links: dict
    attributes: SearchAttributes
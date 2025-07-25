import logging
from typing import Optional, List

from open_webui.retrieval.web.main import SearchResult, get_filtered_results
from ddgs import DDGS
from ddgs.exceptions import RatelimitException
from open_webui.env import SRC_LOG_LEVELS
from open_webui.config import DDG_SAFESEARCH

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


def search_duckduckgo(
    query: str, count: int, filter_list: Optional[list[str]] = None,
    safesearch: str = DDG_SAFESEARCH.value,
) -> list[SearchResult]:
    """
    Search using DuckDuckGo's Search API and return the results as a list of SearchResult objects.
    Args:
        query (str): The query to search for
        count (int): The number of results to return

    Returns:
        list[SearchResult]: A list of search results
    """
    # Use the DDGS context manager to create a DDGS object
    search_results = []
    with DDGS() as ddgs:
        # Use the ddgs.text() method to perform the search
        try:
            search_results = ddgs.text(
                query, safesearch=safesearch, max_results=count, backend="lite"
            )
        except RatelimitException as e:
            log.error(f"RatelimitException: {e}")
    if filter_list:
        search_results = get_filtered_results(search_results, filter_list)

    # Return the list of search results
    return [
        SearchResult(
            link=result["href"],
            title=result.get("title"),
            snippet=result.get("body"),
        )
        for result in search_results
    ]


def search_duckduckgo_images(
    query: str, count: int, safesearch: str = DDG_SAFESEARCH.value
) -> List[str]:
    """Return image URLs from DuckDuckGo image search without duplicates."""
    images: List[str] = []
    seen: set[str] = set()
    with DDGS() as ddgs:
        try:
            for result in ddgs.images(
                query, safesearch=safesearch, max_results=count * 2
            ):
                url = result.get("image") or result.get("thumbnail")
                if url and url not in seen:
                    images.append(url)
                    seen.add(url)
                    if len(images) >= count:
                        break
        except RatelimitException as e:
            log.error(f"RatelimitException: {e}")
    return images

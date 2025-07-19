import logging
from typing import Optional, List

import requests
from open_webui.retrieval.web.main import SearchResult, get_filtered_results
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


def search_brave(
    api_key: str, query: str, count: int, filter_list: Optional[list[str]] = None
) -> list[SearchResult]:
    """Search using Brave's Search API and return the results as a list of SearchResult objects.

    Args:
        api_key (str): A Brave Search API key
        query (str): The query to search for
    """
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key,
    }
    params = {"q": query, "count": count}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    json_response = response.json()
    results = json_response.get("web", {}).get("results", [])
    if filter_list:
        results = get_filtered_results(results, filter_list)

    return [
        SearchResult(
            link=result["url"],
            title=result.get("title"),
            snippet=result.get("description"),
        )
        for result in results[:count]
    ]


def search_brave_images(api_key: str, query: str, count: int) -> List[str]:
    """Return image URLs using Brave's image search API."""
    url = "https://api.search.brave.com/res/v1/images/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key,
    }
    params = {"q": query, "count": count}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        json_response = response.json()
        results = json_response.get("results", [])
        return [item.get("url") for item in results if item.get("url")][:count]
    except Exception as e:
        log.error(f"Error fetching brave images: {e}")
        return []

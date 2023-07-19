import requests
import redis

def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL using the requests module.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    cache_key = f"count:{url}"

    # Connect to Redis
    redis_client = redis.Redis()

    # Check if the URL has been accessed before
    if redis_client.exists(cache_key):
        # Increment the access count for the URL
        redis_client.incr(cache_key)
    else:
        # If the URL is accessed for the first time, set the count to 1 and expire after 10 seconds
        redis_client.setex(cache_key, 10, 1)

    # Fetch the HTML content of the URL using requests
    response = requests.get(url)

    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    html_content = get_page(url)
    print(html_content)

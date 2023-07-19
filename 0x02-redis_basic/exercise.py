import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count how many times a method is called and store the count in Redis.

        Args:
            method (Callable): The method to be decorated.

        Returns:
            Callable: The wrapped method that increments the count and returns the original result.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # Get the qualified name of the method
            key = method.__qualname__
            # Increment the count for the method
            self._redis.incr(key)
            # Call the original method and return its result
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the provided data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in Redis.

        Returns:
            str: The randomly generated key under which the data is stored in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        # ... (unchanged get method)

    def get_str(self, key: str) -> Union[str, None]:
        # ... (unchanged get_str method)

    def get_int(self, key: str) -> Union[int, None]:
        # ... (unchanged get_int method)

# Test cases
cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value

# Get and print the counts for each method
print("store method count:", cache._redis.get("Cache.store"))
print("get method count:", cache._redis.get("Cache.get"))
print("get_str method count:", cache._redis.get("Cache.get_str"))
print("get_int method count:", cache._redis.get("Cache.get_int"))

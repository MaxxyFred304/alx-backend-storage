import redis
import uuid
from typing import Union, Callable, Optional

class Cache:
    def __init__(self):
        """
        Initialize the Cache class and create a Redis client instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
        """
        Retrieve data from Redis associated with the given key and optionally convert it.

        Args:
            key (str): The key associated with the data in Redis.
            fn (Optional[Callable]): A callable function to convert the retrieved data (default=None).

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data in the desired format
                                                 or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is None:
            return data

        return fn(data)

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a string value from Redis associated with the given key.

        Args:
            key (str): The key associated with the string value in Redis.

        Returns:
            Union[str, None]: The retrieved string value or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer value from Redis associated with the given key.

        Args:
            key (str): The key associated with the integer value in Redis.

        Returns:
            Union[int, None]: The retrieved integer value or None if the key does not exist.
        """
        return self.get(key, fn=int)

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

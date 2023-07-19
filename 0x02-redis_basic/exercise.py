import redis
import uuid
from typing import Union, Callable
from functools import wraps

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """
        Decorator to store the history of inputs and outputs for a particular function in Redis.

        Args:
            method (Callable): The method to be decorated.

        Returns:
            Callable: The wrapped method that stores input arguments and output in Redis.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # Get the qualified name of the method
            method_name = method.__qualname__

            # Convert input arguments to string and store in Redis
            inputs_key = f"{method_name}:inputs"
            self._redis.rpush(inputs_key, str(args))

            # Call the original method to get the output
            output = method(self, *args, **kwargs)

            # Store the output in Redis
            outputs_key = f"{method_name}:outputs"
            self._redis.rpush(outputs_key, str(output))

            # Return the output
            return output

        return wrapper

    @call_history
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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
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

# Retrieve and print the input and output history for the store method
print("Input history for store method:", cache._redis.lrange("Cache.store:inputs", 0, -1))
print("Output history for store method:", cache._redis.lrange("Cache.store:outputs", 0, -1))

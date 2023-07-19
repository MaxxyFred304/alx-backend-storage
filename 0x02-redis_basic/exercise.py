from redis import Redis
import uuid
from typing import Union, Callable

def replay(method: Callable):
    """
    Display the history of calls for a particular function.

    Args:
        method (Callable): The method to display the history for.
    """
    method_name = method.__qualname__

    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    redis_client = Redis()
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")

    for input_data, output_data in zip(inputs, outputs):
        input_args = eval(input_data.decode())
        output = output_data.decode()

        print(f"{method_name}(*{input_args}) -> {output}")

class Cache:
    def __init__(self):
        self._redis = Redis()
        self._redis.flushdb()

    @staticmethod
    def call_history(method: Callable) -> Callable:
        # ... (unchanged call_history decorator)

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        # ... (unchanged store method)

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        # ... (unchanged get method)

    def get_str(self, key: str) -> Union[str, None]:
        # ... (unchanged get_str method)

    def get_int(self, key: str) -> Union[int, None]:
        # ... (unchanged get_int method)

# Test case
cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)

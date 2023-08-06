"""
Redis Interface in charge of connecting to redis and performing the requests
"""
import queue
from concurrent.futures import ThreadPoolExecutor
import logging

import redis

logger = logging.getLogger('redis_int')


def only_online(func):
    """Only executes the function if redis is online"""
    def decorator(self, *args, **kwargs):
        if self.is_online():
            return func(self, *args, **kwargs)
    return decorator


class Client:
    """
    Wraps around the traditional redis interface to give some extra functionality like asynchronous calls and others
    """
    async_worker = None

    _redis_client = None
    _executor = None
    _is_online = 0  # -1 offline, 0 not checked, 1 online

    def __init__(self, host: str, port: int = 6379):
        self.host = host
        self.port = port
        self._redis_client = redis.Redis(connection_pool=redis.ConnectionPool(host=host,
                                                                              port=port,
                                                                              socket_timeout=2))
        self._async_exception_queue = queue.SimpleQueue()
        self.asynchronous = async_wrap(self)

    def change_host(self, host: str, port: int = 6379):
        """
        Recreates the redis connection using a new host
        """
        if host == self.host and port == self.port:
            return

        self.host = host
        self.port = port
        self._redis_client = redis.Redis(connection_pool=redis.ConnectionPool(host=host,
                                                                              port=port,
                                                                              socket_timeout=2))

    def check_async_init(self):
        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix='glored')

    def async_call(self, function, args, kwargs):
        if not self._async_exception_queue.empty():
            logger.error('Last async method call got an error, raising now.')
            raise self._async_exception_queue.get(block=False)
        func = getattr(self, function)
        self._executor.submit(self.wrap_async_function(func), *args, **kwargs)

    def wrap_async_function(self, func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f'Received exception in async call: {e}', exc_info=True)
                self._async_exception_queue.put(e)
        return wrapped

    def is_online(self):
        if self._is_online == 1:
            return True
        elif self._is_online == -1:
            return False

        try:
            self.ping()
            self._is_online = 1
            return True
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
            logger.warning('Could not initialize redis. Any call to redis will be ommitted.')
            self._is_online = -1
            return False

    ###########################################
    # Traditional calls
    ###########################################
    def ping(self):
        return self._redis_client.ping()

    @only_online
    def get(self, name):
        return self._redis_client.get(name)

    @only_online
    def set(self, name, value, **kwargs):
        return self._redis_client.set(name, value, **kwargs)

    @only_online
    def publish(self, channel, message, **kwargs):
        return self._redis_client.publish(channel, message, **kwargs)

    @only_online
    def listen(self, channels: list):
        if isinstance(channels, str):
            channels = [channels]

        with redis.client.PubSub(redis.ConnectionPool(host=self.host, port=self.port)) as pubsub:
            for channel in channels:
                pubsub.subscribe(channel)

            for elem in pubsub.listen():
                yield elem


class AsyncWrapper:
    """
    Wraps any _Client function to be queued and asynchronously launched in a thread. Wrapped calls dont return anyting
    """
    def __init__(self, parent_self: Client):
        self.parent_self = parent_self

    def __getattr__(self, item):
        def wraps(*args, **kwargs):
            self.parent_self.check_async_init()
            self.parent_self.async_call(item, args, kwargs)

        return wraps


def async_wrap(parent_self) -> Client:
    return AsyncWrapper(parent_self)

# Asynchronous GLObal REDis Interface

Implements a small interface around the basic `redis.Redis()` client meant to be shared
across different files in the same process that need access to the same redis instance.
This implementation has two major goals:

1. Allow sharing the same Client object across different files without having to pass
the object itself each time.
2. Allow asynchronous calls to the redis interface, specially when submitting data to 
avoid any disruption in running code

## Usage

The usage of this library is straight forward and it implements the basic `redis.Redis()` methods:

```python
from glored import redis_client
import time

# Synchronous
redis_client.set('some_key', 'some_value')
result = redis_client.get('some_key')

# Asynchronous
redis_client.asynchronous.set('some_key', 'other_value')
time.sleep(1)
result = redis_client.get('some_key')
```
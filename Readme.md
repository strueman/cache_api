# Python object API cache system

Store and retrieve Python objects in a centralized cache system. Handy to keep data in memory between runs of a process to avoid having to re-load data or recalculate values. Can be used to share data between unrelated classes or functions. Hold data in memory for fast access. The data is cleared when the server is restarted or shutdown. 

This application provides a simple API-based caching system with a server and client implementation. It allows for storing, retrieving, and managing cached data across different processes. A basic example of how to use the cache is included down below.

## Components

### cache_server.py

This file contains the FastAPI server implementation for the caching system. It provides endpoints for setting, getting, listing, and clearing cached variables. The server uses API key authentication for security.

Key features:
- Set and get variables
- List variables for a specific process
- Clear cache for a process or all processes
- API key authentication

### cache_api.py

This file provides a Python client for interacting with the cache server. It encapsulates the API calls and provides a simple interface for cache operations.

Key features:
- Initialize with process name and load API key from config
- Get and set cache variables
- List cached variables
- Clear cache for a process or all processes

### example_settings.cfg

This is an example configuration file for storing the API key used for authentication between the client and server.

## Usage Example

1. Start the server:
```python
python cache_server.py
```
2. Use the client in your Python code:
```python
from cache_api import APICache
```
### Initialize the cache client
```python
cache = APICache(process_name='example_process')
```
Note: You can leave out the `process_name` parameter if you want to set the `process_name` in each call, usefull for sharing a cache between different processes. So it would be ` cache = APICache()` and then `cache.set_cache('my_var', 'Hello, World!', process_name='example_process')`
### Set a variable
```python
cache.set_cache('my_var', 'Hello, World!')
```
### Get a variable
```python
value = cache.get_cache('my_var')
print(f"Retrieved value: {value}")
```
### List variables
```python
variables = cache.list_cache()
print(f"Variables in cache: {variables}")
```
### Clear process cache
```python
cache.clear_cache()
```
### Clear all cache
```python
cache.clear_all_cache()
```

### Configuration

1. Copy `example_settings.cfg` to `settings.cfg`.
2. An API key will be generated and saved in `settings.cfg` for you on first run.

### Security Note

Ensure that your `settings.cfg` file with the API key is kept secure and not shared publicly.
from abc import ABC, abstractmethod
from collections import OrderedDict
import queue

# Base Asset class
class Asset:
    def __init__(self, asset_id, asset_type, path, size):
        self.id = asset_id
        self.type = asset_type
        self.path = path
        self.size = size
        self.status = "unloaded"
    
    def load(self):
        # Implementation to load the asset from the path
        self.status = "loaded"
        print(f"Asset {self.id} loaded.")
    
    def unload(self):
        # Implementation to unload the asset from memory
        self.status = "unloaded"
        print(f"Asset {self.id} unloaded.")
    
    def get_size(self):
        return self.size

# Base class for Cache Strategy
class CacheStrategy(ABC):
    @abstractmethod
    def cache(self, asset):
        pass

    @abstractmethod
    def evict(self):
        pass

# LRU Caching Strategy implementation
class LRUCachingStrategy(CacheStrategy):
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cache = OrderedDict()

    def cache(self, asset):
        if asset.id in self.cache:
            self.cache.move_to_end(asset.id)
        else:
            if len(self.cache) >= self.cache_size:
                self.evict()
            self.cache[asset.id] = asset
        print(f"Asset {asset.id} cached.")

    def evict(self):
        evicted_asset_id, evicted_asset = self.cache.popitem(last=False)
        evicted_asset.unload()
        print(f"Asset {evicted_asset_id} evicted from cache.")

# Resource Loader class
class ResourceLoader:
    def __init__(self):
        self.loading_tasks = []
    
    def load_asset(self, asset):
        # Implementation of the asset loading logic
        asset.load()
        self.loading_tasks.append(asset)
        self.on_load_complete(lambda: print(f"Loading complete for {asset.id}"))
    
    def unload_asset(self, asset):
        # Implementation of the asset unloading logic
        asset.unload()
    
    def on_load_complete(self, callback):
        callback()

# Priority Queue class
class PriorityQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue()
    
    def enqueue(self, asset, priority):
        self.queue.put((priority, asset))
    
    def dequeue(self):
        priority, asset = self.queue.get()
        return asset

# Asset Manager class (Singleton)
class AssetManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.asset_cache = {}
        self.loading_queue = queue.Queue()
        self.cache_strategy = None
    
    def request_asset(self, asset_id):
        if asset_id in self.asset_cache:
            asset = self.asset_cache[asset_id]
            print(f"Asset {asset_id} retrieved from cache.")
        else:
            asset = Asset(asset_id, "type", "/path/to/asset", 100)  # Example asset creation
            self.loading_queue.put(asset)
            self.load_asset(asset)
        return asset
    
    def release_asset(self, asset_id):
        if asset_id in self.asset_cache:
            asset = self.asset_cache.pop(asset_id)
            self.cache_strategy.evict()
            print(f"Asset {asset_id} released.")
    
    def set_cache_strategy(self, strategy):
        self.cache_strategy = strategy
    
    def update(self):
        while not self.loading_queue.empty():
            asset = self.loading_queue.get()
            self.cache_strategy.cache(asset)
    
    def load_asset(self, asset):
        resource_loader = ResourceLoader()
        resource_loader.load_asset(asset)
        self.asset_cache[asset.id] = asset

# Example Usage
if __name__ == "__main__":
    asset_manager = AssetManager()
    asset_manager.set_cache_strategy(LRUCachingStrategy(cache_size=2))
    
    asset1 = asset_manager.request_asset("asset1")
    asset2 = asset_manager.request_asset("asset2")
    asset3 = asset_manager.request_asset("asset3")
    
    asset_manager.update()  # Update to handle caching
    asset_manager.release_asset("asset1")

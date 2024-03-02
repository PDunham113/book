from abc import ABC, abstractmethod
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Dict, Tuple


TimedItem = Tuple["Cacheable", datetime]
TupleKey = Tuple[Tuple[str, Any], ...]


class CacheError(Exception):
    pass


class Cacheable(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def key(self) -> Dict[str, Any]:
        pass


class TimedLRU:
    EMPTY_RETURN = (None, datetime.min)

    def __init__(self, max_size: int = 128, timeout: float = 30):
        """Timeout in seconds"""
        self._cache_byid: OrderedDict[int, TimedItem] = OrderedDict()
        self._cache_bykey: OrderedDict[TupleKey, TimedItem] = OrderedDict()

        self.max_size: int = max_size
        self.timeout: timedelta = timedelta(seconds=timeout)

    @property
    def size(self) -> int:
        """Return size of cache. If the underlying dicts are not of matching size, complain."""
        if len(self._cache_byid) != len(self._cache_bykey):
            raise CacheError("Cache is out of whack!")
        return len(self._cache_byid)

    def add(self, obj: Cacheable) -> None:
        """Add a Cacheable to the cache. If it's there, mark it as most recently used."""
        # Make our key hashable
        key: TupleKey = tuple(obj.key.items())

        while self.size >= self.max_size and self.max_size > 0:
            for cache in (self._cache_byid, self._cache_bykey):
                cache.popitem(last=False)
        now = datetime.now()
        for cache, k in ((self._cache_byid, obj.id), (self._cache_bykey, key)):
            cache[k] = (obj, now)
            cache.move_to_end(k)

    def get(
        self, id: int | None = None, key: Dict[str, Any | None] = None
    ) -> Cacheable | None:
        """Get a Cacheable by id or by key. If both are provided, prefer id."""
        obj: Cacheable | None = None
        # Make our key hashable
        if key is not None:
            key: TupleKey = tuple(key.items())

        if id is not None and key is not None:
            print("WARN: using `id` instead of provided key")

        if id is not None:
            obj, last_accessed = self._cache_byid.pop(id, self.EMPTY_RETURN)
            if obj is not None:
                self._cache_bykey.pop(tuple(obj.key.items()))
        elif key is not None:
            obj, last_accessed = self._cache_bykey.pop(key, self.EMPTY_RETURN)
            if obj is not None:
                self._cache_byid.pop(obj.id)

        if self.timeout > timedelta(seconds=0)  and last_accessed + self.timeout < datetime.now():
            # Cache element is too old
            # TODO: Should I purge all old elements?
            obj = None

        if obj is not None:
            self.add(obj)

        return obj

    def pop(
        self, id: int | None = None, key: Dict[str, Any | None] = None
    ) -> Cacheable | None:
        """Get and drop a Cacheable by id or by key. If both are provided, prefer id."""
        obj = self.get(id=id, key=key)

        if obj is not None:
            self._cache_byid.pop(obj.id)
            self._cache_bykey.pop(tuple(obj.key.items()))

        return obj

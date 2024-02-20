#!/usr/bin/env python3
import string
import time
import unittest
from typing import Dict

import book.cache


class Item(book.cache.Cacheable):
    def __init__(self, id: int, key: Dict[str, str]):
        self._id = id
        self._key = key

    @property
    def id(self) -> int:
        return self._id

    @property
    def key(self) -> Dict[str, str]:
        return self._key


class TestCache(unittest.TestCase):
    CACHE_SIZE = 10  # Must be smaller than self.items list, greater than 1
    CACHE_TIMEOUT = 1  # Should be a reasonable time - you'll wait for it

    def setUp(self) -> None:
        self.cache = book.cache.TimedLRU(
            max_size=self.CACHE_SIZE, timeout=self.CACHE_TIMEOUT
        )

        self.items = [
            Item(i, {"name": k}) for i, k in enumerate(string.ascii_lowercase)
        ]

    def test__self_test(self):
        """Tests that our test parameters are sane"""
        self.assertTrue(
            1 <= self.CACHE_SIZE <= len(self.items), "CACHE_SIZE is inappropriate"
        )
        self.assertTrue(self.CACHE_TIMEOUT < 5, "CACHE_TIMEOUT is too long")

    def test_add_element(self):
        """Tests element addition, size reporting, and maximum size"""
        self.assertEqual(self.cache.size, 0, "Cache isn't empty at creation")
        self.assertEqual(self.cache.max_size, self.CACHE_SIZE, "Max size isn't correct")

        for i, item in enumerate(self.items[: self.CACHE_SIZE], 1):
            self.cache.add(item)
            self.assertEqual(self.cache.size, i, f"Failed on add {i}")

        self.cache.add(self.items[self.CACHE_SIZE])
        self.assertEqual(self.cache.size, self.CACHE_SIZE, "Cache wasn't bounded")

    def test_retrieve_element(self):
        """Tests retrival of elements from cache"""
        self.cache.add(self.items[0])

        self.assertEqual(self.cache.get(id=0), self.items[0], "Element wasn't there")
        self.assertEqual(self.cache.get(id=1), None, "Element was there?")

        self.assertEqual(
            self.cache.get(key={"name": "a"}), self.items[0], "Element wasn't there"
        )
        self.assertEqual(self.cache.get(key={"name": "b"}), None, "Element was there?")

    def test_timeout(self):
        """Tests that cache elements time out"""
        self.cache.add(self.items[0])
        time.sleep(self.CACHE_TIMEOUT + 0.5)
        self.assertEqual(self.cache.get(id=0), None, "Element didn't time out")

    def test_errors(self):
        """Tests raising of error on cache mismatch"""
        self.cache.add(self.items[0])
        self.cache._cache_byid = {}

        with self.assertRaises(
            book.cache.CacheError, msg="Cache doesn't report size mismatch"
        ):
            self.cache.size


if __name__ == "__main__":
    unittest.main()

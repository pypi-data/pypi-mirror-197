from __future__ import annotations

import collections
import copy
import heapq
from typing import Generic, TypeVar, Iterable, Callable, Iterator

from comparablevalue import ComparableValue

T = TypeVar('T')
C = TypeVar('C', bound=ComparableValue)


def identity(arg):
    return arg


def unlink(heap, key) -> object:
    item = heap.map[key].pop()
    if len(heap.map[key]) == 0:
        del heap.map[key]
    return item


class heap(Generic[T]):
    """
    A simple wrapper class around Python's built in `heapq` module. Implements a
    priority queue as a min-heap. The heap invariant is maintained only at the bounds of method calls.
    Within a method call the heap invariant may not hold
    """

    def __init__(self, iterable: Iterable[C] | None = None, key: Callable[[T], C] | None = None):
        """
        Creates a heap with the given iterable. iterable is heapified before the end of the __init__ call.
        If iterable is None, an empty heap is created. The element type of this collection must adapt the
        ComparableValue protocol. See the ComparableValue protocol in comparablevalue.py for more

        key determines how the elements of the heap are ordered. It should take a single item of the type 
        of the elements of the heap and return anything that is comparable.
        :param: iterable - the collection to heapify and store or None 
        :param: key - a function that takes elements of the heap and produces the comparable value on which they are organized 
        """
        self.key = key if key is not None else identity
        self.map = collections.defaultdict(list)
        if iterable is None:
            self.backing = []
        else:
            self.backing = [key(i) for i in iterable]
            for i in iterable:
                self.map[key(i)].append(i)
            heapq.heapify(self.backing)

    @property
    def smallest(self):
        """
        Returns the smallest element in the heap in O(1) time
        :return: the smallest element in the heap
        """
        return self.map[self.backing[0]][0]

    @property
    def top(self):
        """
        Returns the top of the heap in O(1) which is the smallest element
        :return: the top of the heap
        """
        return self.smallest

    def push(self, item: Iterable[T] | T) -> None:
        """
        Add an item or a collection of items to the heap.

        If `item` is a single value, it is pushed onto the heap maintaining the heap invariant
        If `item` is a collection, the collection is concatenated to the end of the heap and then the heap if heapified.
        when this happens the heap invariant is broken until the return of this method

        :param item: an item or collection of items to add to the heap
        """
        try:
            self.backing.extend(self.key(i) for i in item)
            for i in item:
                self.map[self.key(i)].append(i)
            heapq.heapify(self.backing)
        except TypeError:
            heapq.heappush(self.backing, self.key(item))
            self.map[self.key(item)].append(item)

    def pop(self) -> T:
        """
        Removes and returns the smallest element (i.e. the top) of the heap
        :return: the smallest element (i.e. the top) of the heap
        """

        key = heapq.heappop(self.backing)
        return unlink(self, key)

    def pushpop(self, item: T) -> T:
        """
        Push item on the heap, then pop and return the smallest (i.e. top) item from the heap.
        The combined action runs more efficiently than heap.push() followed by a separate call to heap.pop().
        :param item: the item to add to the heap
        :return: the smallest item on the heap after the push
        """
        key = heapq.heappushpop(self.backing, self.key(item))
        return unlink(self, key)

    def replace(self, item: T) -> T:
        """
        Pop and return the current smallest value, and add the new item.
        This is more efficient than heap.pop() followed by heap.push(), and can be more appropriate when using a
        fixed-size heap. Note that the value returned may be larger than item! That constrains reasonable uses of
        this routine unless written as part of a conditional replacement:

        if item > heap[0]:
            item = heapreplace(heap, item)
        :param item: the item to add to the heap
        :return: the smallest item on the heap *before* the push
        """
        key = heapq.heapreplace(self.backing, self.key(item))
        return unlink(self, key)

    def __add__(self, other: Iterable[T] | T) -> heap[T]:
        """
        Creates a copy of self, then returns the copy after copy += other is performed
        :param other: an element or collection of elements to add to the heap
        :return: a new heap containing the elements of self and other
        """
        try:
            this = copy.copy(self)
            this += other
            return this
        except TypeError:
            return NotImplementedError

    def __iadd__(self, other: Iterable[T] | T) -> None:
        """
        If a is a heap and b is an element, iterable, or heap, then a += b is equivalent to a.push(b)
        :param other:
        :return:
        """
        try:
            self.push(other)
        except TypeError:
            return NotImplementedError

    def __iter__(self) -> Iterator[T]:
        """
        Returns the elements of the heap in an unspecified order with no guarantee *except* that the smallest element
        is the heap will be first
        :return: An iterable of elements in the heap
        """
        return iter(self.backing)

    def __eq__(self, o: object) -> bool:
        """
        Returns true if isinstance(o, heap) and for every element, e, in self, e is in o, and for every element, j, in
        o, j is in self *regardless of order*
        :param o:
        :return:
        """
        if not isinstance(o, heap):
            return False
        s1 = self.map
        s2 = o.map
        return all(i in s1 for i in s2) and all(j in s2 for j in s1)

    def __ne__(self, o: object) -> bool:
        """
        returns not (self == o)
        :param o: see __eq__
        :return: not (self == o)
        """
        return not (self == o)

    def __str__(self) -> str:
        return '[{}]'.format(', '.join(str(self.map[i]) for i in self.backing))

    def __repr__(self) -> str:
        return 'Heap({}{})'.format(', '.join(str(self.map[i]) for i in self.backing),
                                   ", key={}".format(self.key) if self.key != identity else '')

    def __hash__(self) -> int:
        return hash(~hash(0xdeadbeef) - hash(0xcafecafe) + hash(set(self.backing)))

    def __len__(self):
        return len(self.backing)

    def clear(self):
        self.backing = []
        self.map = collections.defaultdict(list)

    @staticmethod
    def parent_index(index: int) -> int:
        return (index - 1) // 2

    @staticmethod
    def child_indices(parent: int) -> tuple[int, int]:
        return (parent * 2), (parent * 2 + 1)

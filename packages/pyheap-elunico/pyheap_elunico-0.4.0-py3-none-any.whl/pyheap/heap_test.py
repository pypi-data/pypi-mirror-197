import random
import unittest

from .heap import heap


class MyTestCase(unittest.TestCase):
    def test_smallest_single_ascending(self):
        h = heap()
        h.push(1)
        h.push(2)
        h.push(3)
        self.assertEqual(h.smallest, 1)

    def test_smallest_single_descending(self):
        h = heap()
        h.push(3)
        h.push(2)
        h.push(1)
        self.assertEqual(h.smallest, 1)

    def test_smallest_single_random(self):
        h = heap()
        placed = False
        for i in range(200):
            if random.random() < 0.1 and not placed:
                h.push(-2)
                placed = True
            else:
                h.push(random.randint(0, 1000))
        self.assertEqual(h.smallest, -2)

    def test_smallest_no_elements(self):
        def action():
            h = heap()
            self.assertIsNotNone(h.smallest)

        self.assertRaises(IndexError, action)

    def test_smallest_multiple_ascending(self):
        h = heap()
        h.push([1, 2, 3, 4, 5])
        self.assertEqual(h.smallest, 1)

    def test_smallest_multiple_descending(self):
        h = heap()
        h.push([5, 4, 3, 2, 1])
        self.assertEqual(h.smallest, 1)

    def test_smallest_multiple_random(self):
        h = heap()
        placed = False
        while not placed:
            if random.random() < 0.1 and not placed:
                h.push([-2])
                placed = True
            else:
                h.push([random.randint(0, 1000) for j in range(10)])
        self.assertEqual(h.smallest, -2)

    def test_smallest_eq_top(self):
        h = heap()
        for j in range(50):
            for x in range(2300):
                h.push(x)
            self.assertEqual(h.top, h.smallest)
            h = heap()

    def test_clear(self):
        h = heap()
        h.push([5, 3, 5, 7, 1, 2, 3])
        self.assertEqual(h.smallest, 1)
        h.clear()
        self.assertEqual(len(h), 0)
        h.push(0)
        self.assertEqual(h.smallest, 0)

    def test_heap_invariant(self):
        h = heap()
        for i in range(3000):
            h.push(random.randint(0, 10000))

        def parent(child_idx):
            return (child_idx - 1) // 2

        all(self.assertLessEqual(h.pop(), h.smallest) for (i, elt) in enumerate(h.backing))


if __name__ == '__main__':
    unittest.main()

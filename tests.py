import unittest
import time
import os

from event_counter import EventCounter
from event_counter.compat import xrange


class EventCounterTest(unittest.TestCase):

    def is_travis(self):
        """Test if we are running in Travis"""
        return "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true"


    def test_buffer_contents_simple(self):
        n_events = 100

        t = EventCounter(3)

        for _ in xrange(n_events):
            t.save()

        self.assertEqual(list(t._buffer), [0, 0, n_events])


    def test_buffer_contents_with_sleep(self):
        n_events = 100

        t = EventCounter(3)

        for _ in xrange(n_events):
            t.save()

        time.sleep(2)
        t.save()

        self.assertEqual(list(t._buffer), [n_events, 0, 1])


    def test_buffer_contents_with_sleep_slow_events(self):
        t = EventCounter(5)

        t.save() # 1 event to bin 1

        time.sleep(1.2) # 3 events to bin 2
        for _ in xrange(3):
            t.save()

        time.sleep(1.9) # 0 events to bin 3, 1 event to bin 4
        t.save()

        time.sleep(0.9) # 1 event to bin 5
        t.save()

        self.assertEqual(list(t._buffer), [1, 3, 0, 1, 1])


    def test_speed_write(self):
        """Testing saving events at a rate greater than some threshold"""
        buffer_size = 3
        max_rate = int(1e6) if not self.is_travis() else int(1e5) # events/s
        n_events = buffer_size * max_rate

        t = EventCounter(buffer_size) # each buffer element has to take at least `max_rate` events

        for _ in xrange(n_events):
            t.save()

        self.assertEqual(t.read(), n_events)


    def test_speed_read(self):
        """Testing reading events at a rate greater than some threshold"""
        max_rate = int(1e4) if not self.is_travis() else int(1e3) # reads/s

        t = EventCounter()
    
        for _ in xrange(max_rate):
            t.save()
            t.read()
        # after `max_rate` reads and writes we should still be within last active bin 
        # containing `max_rate` events
        self.assertEqual(t.read(1), max_rate)


    def test_counter_empty(self):
        t = EventCounter()
        self.assertEqual(t.read(), 0)


    def test_arg_malformed_nonsense(self):
        for nonsense in (False, None, 'nonsense', -5, 0, 1.1, 1e4, [0]):
            t = EventCounter(nonsense)
            self.assertEqual(t.read(), 0)
            t.save()
            self.assertEqual(t.read(nonsense), 1)


    def test_arg_malformed_read(self):
        t = EventCounter()
        t.save()
        self.assertEqual(t.read(1000), 1)


    def test_read(self):
        t = EventCounter()
        self.assertEqual(t.read(1), 0)
        t.save()
        time.sleep(1)
        self.assertEqual(t.read(1), 0)


if __name__ == '__main__':
    unittest.main()
    
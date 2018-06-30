import unittest
import aiounittest
import asyncio

from DataAnalysis.ProcessingTools.Queues.QueueTools import SaveQueueHandler
from tests.helpers.Factories import DummyIListenerFactory

class SaveQueueHandlerTests(unittest.TestCase ):

# class SaveQueueHandlerTests(aiounittest.AsyncTestCase ):

    def setUp(self):
        self.object = SaveQueueHandler()
        self.listener = DummyIListenerFactory()

    def test_next(self):
        self.object.listeners.append(self.listener)
        # call
        # future = asyncio.Future()
        result = self.object.next( )

        # result = await self.object.next( )
        self.assertEqual(result, self.listener)

# async def test_enque(self):

    def test_enque(self):
        item = [1, 2]

        # call
        # future = asyncio.Future()
        # r = await self.object.enque( item)
        self.object.enque( item)

        # check
        self.assertEqual(1, self.listener.handle_call_count, "Listener handle was called")
        self.assertEqual(self.listener.queue[0], item)

    def test_register_listener(self):
        self.object.register_listener(self.listener)
        self.assertEqual(len(self.object.listeners, 1))
        self.assertEqual(self.object.listeners[0], self.listener)

    def test_notify_new_item_in_queue(self):
        """Call the handle methnd on each registered listener, passing
        the queueHandler as the argument"""
        # if PRINT_STEPS is True: print("SaveQueueHandler.notify_new_item_in_queue()")
        # [l.handle(self) for l in self.listeners]
        pass


if __name__ == '__main__':
    unittest.main()

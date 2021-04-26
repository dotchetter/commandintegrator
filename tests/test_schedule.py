import asyncio
import functools
import time
import unittest
from datetime import datetime
from unittest import TestCase
import commandintegrator as ci


class Reciever:
    async def async_recieve(self, msg=None):
        print("Async receiver:", msg)

    def recieve(self, msg=None):
        print("Sync receiver:", msg)



if __name__ == "__main__":

    def test_sync():

        class User:

            def __init__(self, name):
                self.name = name

            @ci.scheduler.asyncmethod(every="second")
            async def get_name_async(self):
                return f"Hi, my name is {self.name} asynchronously"

            @ci.scheduler.method(every="second")
            def get_name(self):
                return f"Hi, my name is {self.name} synchronously"

        def regular_method_addition(a, b):
            return a + b

        def say_hello():
            return "Hello sync!"

        user_1 = User(name="user1")
        addition = ci.scheduler.run(regular_method_addition,
                                    every="second", kwargs={"a": 250, "b": 250}, run_now=False)
        ci.scheduler.run(say_hello, every="second", run_now=False)

        ci.scheduler.start_scheduled_method(user_1.get_name)
        ci.scheduler.start_scheduled_method(addition, 45, 45)
        # For decorated
        ci.scheduler.start_scheduled_method(regular_method_addition, 1, 2)

        while 1:
            time.sleep(0.01)
            if ci.scheduler.has_outputs():
                print(ci.scheduler.outputs.get())

    def test_async():

        class User:

            def __init__(self, name):
                self.name = name

            @ci.scheduler.asyncmethod(every="second")
            async def get_name_async(self):
                return f"Hi, my name is {self.name} asynchronously"

            @ci.scheduler.method(every="second")
            def get_name(self):
                return f"Hi, my name is {self.name} synchronously"

        @ci.scheduler.asyncmethod(every="second", delay="00:00:05", kwargs={"something": "Five seconds"})
        async def async_say_something(something):
            return f"Hello {something}!"

        # @ci.scheduler.asyncmethod(every="second", delay="00:00:10", kwargs={"a": 45, "b": 0})
        async def async_regular_method_addition(a, b):
            return a + b

        user_2 = User(name="user2")

        print(async_say_something)
        """
        ci.scheduler.start_scheduled_method(async_say_something, "run_async")

        ci.scheduler.run_async(async_say_something, every="second", delay="00:00:05",
                               kwargs={"something": "five sec"})

        ci.scheduler.run_async(async_say_something, every="second", delay="00:00:02",
                               kwargs={"something": "two sec"})
        """
        print(async_say_something)

        # For decorated
        ci.scheduler.start_scheduled_method(user_2.get_name_async)

        while 1:
            time.sleep(0.01)
            if ci.scheduler.has_outputs():
                print(ci.scheduler.outputs.get())
                print(asyncio.run(user_2.get_name_async()))

    test_async()

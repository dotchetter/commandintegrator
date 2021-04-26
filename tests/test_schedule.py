import asyncio
import threading
import time
import unittest
from datetime import datetime, timedelta
from unittest import TestCase
import commandintegrator as ci


class Reciever:
    async def async_recieve(self, msg=None):
        print("Async receiver:", msg)

    def recieve(self, msg=None):
        print("Sync receiver:", msg)


class User:
    def __init__(self, name):
        self.name = name

    async def get_name_async(self):
        return f"Hi, my name is {self.name} asynchronously"

    def get_name(self):
        return f"Hi, my name is {self.name} synchronously"

    async def say_something_async(self, something: str):
        return f"I say {something} async"

    def say_something(self, something: str):
        return f"I say {something}"


@ci.logger.loggedmethod
def add_numbers(x, y):
    return x + y


if __name__ == "__main__":

    reciever = Reciever()

    user = User(name="user")

    ci.schedule.method(user.get_name,
                       exactly_at=datetime.now() + timedelta(seconds=10))

    ci.schedule.method(user.say_something_async, every="second",
                       something="run_async", start_now=False)

    ci.schedule.method(user.say_something, every="second",
                       something="every second async")

    ci.schedule.method(add_numbers, every="second", x=1, y=2,
                       recipient=reciever.async_recieve)

    print("Unstarted jobs:", ci.schedule.get_unstarted_jobs())

    while 1:
        time.sleep(1)

        print(user.say_something(something="called explicitly"))

        if ci.schedule.has_outputs():
            job = ci.schedule.outputs.get()
            print(job.native_id, "said:", job.result)

import sys
from unittest import TestCase
import time
import unittest
from datetime import datetime, timedelta
from unittest import TestCase
import commandintegrator as ci
from commandintegrator.tools.scheduling.components import Job


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


class Testschedule(TestCase):

    def setUp(self) -> None:
        self.user_mock = User(name="user")
        self.reciever_mock = Reciever()

    def test_scheduling(self):
        # Schedule an instance method
        ci.schedule.method(self.user_mock.get_name,
                           every="second")

        # Make sure it's scheduled
        self.assertTrue(ci.schedule.get_jobs("get_name"),
                        "Scheduled method was not found to be scheduled")

        # Make sure it's running
        self.assertTrue(next(ci.schedule.get_jobs("get_name")).running)

        # Make sure it's a Job which is recieved when calling get_jobs
        recieved_job = next(ci.schedule.get_jobs("get_name"))
        self.assertIsInstance(recieved_job, Job)

        # Make sure the output is in the schedule.outputs
        time.sleep(5)
        self.assertTrue(ci.schedule.has_outputs(),
                        "There were no outputs in schedule.outputs")

        # Get the output and ensure it's the job
        job = ci.schedule.outputs.get()
        self.assertIs(recieved_job, job, "The jobs do not match")

        # Schedule a new job and assert it is not running
        ci.schedule.method(self.user_mock.say_something_async, every="second",
                           something="run_async", start_now=False)
        self.assertIn(next(ci.schedule.get_jobs("say_something_async")),
                      ci.schedule.get_unstarted_jobs(), "Unstarted job was not in "
                                                        "schedule.get_unstarted_jobs")


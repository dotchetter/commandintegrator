import time
from datetime import datetime, timedelta
from unittest import TestCase, skip
import commandintegrator as ci
from functools import partial


async def recieve(msg=None):
    print("Async receiver:", msg)


class TimeFeature:

    def __init__(self, name):
        self.name = name
        # super().__init__()
        # self.command_parser = ci.CommandParser(keywords="klockan")
        # self.command_parser.callbacks = ci.Callback("klockan", self.get_time)
        # ci.schedule.run(self.get_time, )

    @ci.schedule.run(every="second", kwargs={"country": "sverige", "greeting": "hej"})
    def get_time(self, country=None, greeting=None):
        return f"{greeting}! Klockan är {datetime.now().strftime('%H:%M')} i {country}, {self}"

    @ci.schedule.run(every="second", recipient=recieve)
    def no_args(self):
        return f"I just return this string as async: {self}"


if __name__ == "__main__":

    tf = TimeFeature(name="hejsan")

   #@ci.schedule.run(after="00:00:05", every="second")
    def two_seconds():
        return "five seconds!"

    #@ci.schedule.run(every="second")
    async def hello_world():
        return "hello world"

    # ci.schedule.schedule(func=hello_world, every="minute")

    now = datetime.now()
    now += timedelta(seconds=5)

    @ci.schedule.run(exactly_at=now)
    def thankgoditsfriday():
        return f"I ran {datetime.now()}"
    while 1:
        time.sleep(0.01)
        job = ci.schedule.outputs.get()
        if job:
            print(job.result)

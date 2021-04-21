import asyncio
import time
from datetime import datetime
import commandintegrator as ci


class TimeFeature:

    def __init__(self, offset=0):
        self.minutes = 0 + offset

    @ci.scheduler.method(every="wednesday", at="21:46",
                         kwargs={"country": "sverige", "greeting": "hej"})
    def get_time(self, country=None, greeting=None):
        return f"{greeting}! Klockan är {datetime.now().strftime('%H:%M')} i {country}"

    @ci.scheduler.method(every="second")
    def get_minutes(self, arg=1):
        self.minutes += arg
        return f"{self.minutes} seconds passed"


async def recieve(msg=None):
    print("Async receiver:", msg)


@ci.scheduler.method(every="second", delay="00:00:15", kwargs={"a": 1, "b": 2}, recipient=print)
def get_sum(a, b, c=0):
    return a + b + c


class User:

    def __init__(self, name):
        self.name = name

    @ci.scheduler.method(every="second", delay="00:00:10", recipient=print)
    async def get_name(self):
        return self.name


if __name__ == "__main__":

    # ci.scheduler.allow_multiple = True

    print("*" * 50, sep="")

    get_sum(1, 1)

    urban = User(name="urban")
    tomas = User(name="tomas")

    print(ci.scheduler.unstarted)

    print(asyncio.run(urban.get_name()))
    print(asyncio.run(tomas.get_name()))

    print(ci.scheduler.unstarted)

    # Simulerar main loop
    while 1:
        time.sleep(0.01)
        if ci.scheduler.has_outputs():
            print(ci.scheduler.outputs.get())

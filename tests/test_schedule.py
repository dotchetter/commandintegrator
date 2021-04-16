import time
from datetime import datetime
from unittest import TestCase, skip
from commandintegrator.core.decorators import schedule


async def recieve(msg=None):
    print("The Foo.recieve got:", msg)


if __name__ == "__main__":

    @schedule.method(every="second", kwargs={"what": "wohooo!"})
    async def say(what):
        raise AttributeError("This is constructed")
        return f"{datetime.now().strftime('%H:%M:%S')}: {what}"

    # @schedule.method(after="00:00:05")
    def two_seconds():
        return "Two seconds!"

    #@schedule.method(every="second")
    async def every_second():
        return datetime.now().strftime("%H:%M:%S")

    # @schedule.method(every="friday", at="09:00")
    def thankgoditsfriday():
        return "Thank god its friday!"

    while 1:
        time.sleep(1)
        if job := schedule.outputs.get():
            print("\r", job, end="")
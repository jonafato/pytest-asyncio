import asyncio
import sys

import pytest

collect_ignore = []
if sys.version_info[:2] < (3, 6):
    collect_ignore.append("async_fixtures/test_async_gen_fixtures_36.py")
    collect_ignore.append("async_fixtures/test_nested_36.py")


@pytest.yield_fixture()
def dependent_fixture(event_loop):
    """A fixture dependent on the event_loop fixture, doing some cleanup."""
    counter = 0

    @asyncio.coroutine
    def just_a_sleep():
        """Just sleep a little while."""
        nonlocal event_loop
        yield from asyncio.sleep(0.1, loop=event_loop)
        nonlocal counter
        counter += 1

    event_loop.run_until_complete(just_a_sleep())
    yield
    event_loop.run_until_complete(just_a_sleep())

    assert counter == 2

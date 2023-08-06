import pytest

import offloading

MP_PARAMS = [
    ([], {}),
    ([1, 2], {}),
    ([3], {"y": 4}),
    ([], {"x": 5, "y": 6}),
]


def get_result(x=None, y=None):
    return dict(x=x, y=y)


@offloading.offload
def decorated_get_result(*args, **kwargs):
    return get_result(*args, **kwargs)


def get_error(e):
    raise e


def get_killed():
    import os
    import signal

    os.kill(os.getpid(), signal.SIGKILL)


@pytest.mark.parametrize(
    "args, kwargs",
    MP_PARAMS,
)
def test_task(args, kwargs):
    task = offloading.Task(f"{__name__}.get_result", *args, **kwargs)
    assert isinstance(task, offloading.Task)
    assert not task.process.is_alive()
    future = task.start()
    assert future.result(0.1) == get_result(*args, **kwargs)


def test_decorator():
    assert decorated_get_result(1, 2) == get_result(1, 2)


def test_task_timeout():
    with pytest.raises(offloading.TimeoutError):
        offloading.Task.run("time.sleep", 1).result(0.1)


class SampleError(Exception):
    pass


def test_expected_error():
    future = offloading.Task.run(f"{__name__}.get_error", SampleError)
    with pytest.raises(SampleError):
        future.result(1)


def test_unexpected_error():
    future = offloading.Task.run(f"{__name__}.get_killed")
    with pytest.raises(offloading.ProcessAborted):
        future.result(1)

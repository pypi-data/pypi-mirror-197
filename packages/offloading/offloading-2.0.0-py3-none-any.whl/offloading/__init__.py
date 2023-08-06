from __future__ import annotations

import multiprocessing as mp
import threading
import types
import typing as t
from concurrent.futures import _base
from functools import wraps
from importlib import import_module
from multiprocessing.connection import Connection
from traceback import format_exception

Future = _base.Future
TimeoutError = _base.TimeoutError


class ProcessAborted(Exception):
    pass


class RemoteTraceback(Exception):
    def __init__(self, tb: str) -> None:
        self.tb = tb

    def __str__(self) -> str:
        return self.tb


class ExceptionWithTraceback:
    def __init__(self, exc: BaseException, tb: types.TracebackType) -> None:
        self.exc = exc
        # Traceback object needs to be garbage-collected as its frames
        # contain references to all the objects in the exception scope
        self.exc.__traceback__ = None
        tb_str = "".join(format_exception(type(exc), exc, tb))
        self.tb = f'\n"""\n{tb_str}"""'

    def __reduce__(self) -> t.Tuple[t.Callable, t.Tuple[BaseException, str]]:
        return _rebuild_exc, (self.exc, self.tb)


def _rebuild_exc(exc: BaseException, tb: str) -> BaseException:
    exc.__cause__ = RemoteTraceback(tb)
    return exc


class Pipe(t.NamedTuple):
    reader: Connection
    writer: Connection

    @classmethod
    def new(cls, duplex=False) -> "Pipe":
        return cls(*mp.Pipe(duplex=duplex))


class Task:
    POLL_INTERVAL = 0.1

    __slots__ = (
        "target",
        "args",
        "kwargs",
        "future",
        "pipe",
        "thread",
        "process",
    )

    def __init__(self, target: str | t.Callable, *args: t.Any, **kwargs: t.Any) -> None:
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.future: Future = Future()
        self.pipe: Pipe = Pipe.new()
        self.thread = threading.Thread(target=self)
        self.process: mp.Process = mp.Process(target=self._run, args=(self.target, *self.args), kwargs=self.kwargs)

    __class_getitem__ = classmethod(types.GenericAlias)

    def __call__(self) -> None:
        if not self.future.set_running_or_notify_cancel():
            return
        try:
            while not self.pipe.reader.poll(self.POLL_INTERVAL):
                if not self.process.is_alive():
                    self.future.set_exception(ProcessAborted())
                    return
            value, is_exception = self.pipe.reader.recv()
            if is_exception:
                self.future.set_exception(value)
            else:
                self.future.set_result(value)
        finally:
            self.pipe.reader.close()
            self.process.join()
            self.process.close()
            self.pipe = None
            self.thread = None
            self.process = None

    def start(self) -> Future:
        self.thread.start()
        self.process.start()
        return self.future

    @classmethod
    def run(cls, target: str | t.Callable, *args: t.Any, **kwargs: t.Any) -> Future:
        return cls(target, *args, **kwargs).start()

    def _run(self, target: str | t.Callable, *args: t.Any, **kwargs: t.Any) -> None:
        value = None
        is_exception = True
        try:
            if isinstance(target, str):
                module_name, func_name = target.rsplit(".", 1)
                module = import_module(module_name)
                func = getattr(module, func_name)
                if hasattr(func, "__wrapped__"):
                    func = func.__wrapped__
                func = t.cast(t.Callable, func)
            else:
                func = target
            value = func(*args, **kwargs)
            is_exception = False
        except BaseException as e:
            value = ExceptionWithTraceback(e, e.__traceback__)
        finally:
            self.pipe.writer.send((value, is_exception))
            self.pipe.writer.close()


def offload(func: t.Callable) -> t.Callable:
    @wraps(func)
    def wrapper(*args: t.Any, **kwargs: t.Any):
        return Task.run(f"{func.__module__}.{func.__name__}", *args, **kwargs).result()

    wrapper.__wrapped__ = func  # type: ignore [attr-defined]
    return wrapper

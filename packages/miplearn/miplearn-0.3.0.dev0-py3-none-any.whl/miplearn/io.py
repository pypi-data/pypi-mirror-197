#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020-2022, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.

from gzip import GzipFile
import os
import pickle
import sys
from typing import IO, Any, Callable, List, cast, TextIO

from .parallel import p_umap
import shutil


class _RedirectOutput:
    def __init__(self, streams: List[Any]) -> None:
        self.streams = streams

    def write(self, data: Any) -> None:
        for stream in self.streams:
            stream.write(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()

    def __enter__(self) -> Any:
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = cast(TextIO, self)
        sys.stderr = cast(TextIO, self)
        return self

    def __exit__(
        self,
        _type: Any,
        _value: Any,
        _traceback: Any,
    ) -> None:
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


def save(
    objs: List[Any],
    dirname: str,
    prefix: str = "",
    n_jobs: int = 1,
    progress: bool = False,
) -> List[str]:
    filenames = [f"{dirname}/{prefix}{i:05d}.pkl.gz" for i in range(len(objs))]

    def _process(i: int) -> None:
        filename = filenames[i]
        obj = objs[i]
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with GzipFile(filename, "wb") as file:
            pickle.dump(obj, cast(IO[bytes], file))

    p_umap(
        _process,
        range(len(objs)),
        smoothing=0,
        num_cpus=n_jobs,
        maxtasksperchild=None,
        disable=not progress,
    )
    return filenames


def load(filename: str, build_model: Callable) -> Any:
    with GzipFile(filename, "rb") as file:
        data = pickle.load(cast(IO[bytes], file))
        return build_model(data)


def gzip(filename: str) -> None:
    with open(filename, "rb") as input_file:
        with GzipFile(f"{filename}.gz", "wb") as output_file:
            shutil.copyfileobj(input_file, output_file)
    os.remove(filename)

import asyncio
import gzip
import http
import io
from functools import partial, wraps
from typing import Awaitable, Callable, Iterator, Optional, Union

import requests
import requests.adapters

from . import __version__


# General helpers
def to_async(sync_func: Callable) -> Callable:
    @wraps(sync_func)
    async def _async_func(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_running_loop()
        pfunc = partial(sync_func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return _async_func


# Async file handling
class FileWrapper:
    _file: io.FileIO
    _write: Callable[[Union[str, bytes]], Awaitable[int]]
    _close: Callable[[], Awaitable[None]]

    def __init__(self, file: io.FileIO) -> None:
        self._file = file
        self._write = to_async(self._file.write)
        self._close = to_async(self._file.close)

    async def close(self) -> None:
        await self._close()

    async def write(self, data: Union[str, bytes]) -> int:
        return await self._write(data)


class File:
    _path: str
    _mode: str
    _open: Callable[[str, str], Awaitable]
    _file: FileWrapper

    def __init__(self, path: str, mode: str) -> None:
        self._path = path
        self._mode = mode
        self._open = to_async(open)

    async def __aenter__(self) -> FileWrapper:
        _gzip_file: io.FileIO = await self._open(self._path, self._mode)
        self._file = FileWrapper(_gzip_file)
        return self._file

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        return await self._file.close()


class GzipStreamReader:
    _fileobj: gzip.GzipFile
    _readline: Callable[[], Awaitable[Union[str, bytes]]]

    def __init__(self, stream: io.BufferedIOBase):
        self._fileobj = gzip.GzipFile(fileobj=stream, mode="r")
        self._readline = to_async(self._fileobj.readline)

    def __enter__(self) -> "GzipStreamReader":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._fileobj.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self._readline()
        if not line:
            raise StopAsyncIteration
        return line


# Async 'requests' wrapper
class AsyncIterator:
    _iterator: Iterator
    _iterator_anext: Callable[[], Awaitable[bytes]]

    def __init__(self, iterator: Iterator):
        self._iterator = iterator

    def __aiter__(self):
        self._iterator = self._iterator.__iter__()
        self._iterator_anext = to_async(self.__next_wrapper__)
        return self

    async def __anext__(self):
        return await self._iterator_anext()

    def __next_wrapper__(self):
        try:
            return self._iterator.__next__()
        except StopIteration:
            raise StopAsyncIteration()


class ResponseStream(io.BufferedIOBase):
    DEFAULT_BUFFER_SIZE = 1024000  # 1 MB

    _buffer_size: int
    _buffer: bytearray
    _read_offset: int
    _eof_offset: int

    def __init__(
        self,
        response: requests.Response,
        buffer_size: int = DEFAULT_BUFFER_SIZE,
    ) -> None:
        self._buffer_size = buffer_size
        self._read_offset = buffer_size  # Force to pull on first read
        self._eof_offset = -1  # EOF not yet reached
        self._response_iterator = response.iter_content(buffer_size, False)
        self._buffer = bytearray(buffer_size)

    def read(self, size: Optional[int] = DEFAULT_BUFFER_SIZE) -> bytes:
        """
        Read and return up to a number of 'size' bytes. An empty bytes object is returned if the stream is already at EOF.
        This method is inherited from io.BufferedIOBase that allows 'size' to be None or negative but this implementation
        raises a ValueError in these cases.

        :param size: The number of bytes to be returned.
        :returns: An array of bytes.
        :raises ValueError: If 'size' is None or negative.
        """
        if size is None or size < 0:
            raise ValueError(
                "Value of 'size' argument must be a non-negative integer (None or -1 is not supported)!"
            )

        if size == 0:
            return bytes()

        result = bytearray(size)
        result_offset = 0

        while True:
            self._pull_data()
            read_count = self._readinto(result, result_offset)
            if read_count == 0:
                break
            result_offset += read_count

        return bytes(result[0:result_offset])

    def _pull_data(self):
        if self._eof_offset != -1:
            # EOF reached, no more data to pull.
            return

        if self._read_offset != self._buffer_size:
            # End of buffer not yet reached, no need to pull.
            return

        # End of buffer reached -> Pull the next chunk of data
        next_chunk = next(self._response_iterator, None)
        if next_chunk is None:
            self._eof_offset = 0
        elif len(next_chunk) < self._buffer_size:
            self._eof_offset = len(next_chunk)

        # Copy the pulled data into the buffer and start reading from the beginning
        self._buffer[0 : len(next_chunk)] = next_chunk
        self._read_offset = 0

    def _readinto(self, target: bytearray, offset: int) -> int:
        if offset < 0:
            raise ValueError(
                "Value of 'offset' argument must be a non-negative integer!"
            )

        if offset >= len(target):
            return 0

        # Determine the number of bytes to read
        max_read_count = (
            (self._eof_offset - self._read_offset)
            if self._eof_offset != -1
            else (self._buffer_size - self._read_offset)
        )
        actual_read_count = min(len(target) - offset, max_read_count)

        # Read the determined number of bytes into the target
        target[offset : offset + actual_read_count] = self._buffer[
            self._read_offset : self._read_offset + actual_read_count
        ]
        self._read_offset += actual_read_count
        return actual_read_count


class AsyncStreamResponse:
    DEFAULT_CHUNK_SIZE = 1024000  # 1 MB

    _get_as_stream_func: Callable[[], Awaitable[requests.Response]]
    _response: requests.Response
    _close: Callable[[], Awaitable[None]]
    _text: Callable[[], Awaitable[str]]

    def __init__(self, get_as_stream_func: Callable[[], Awaitable[requests.Response]]):
        self._get_as_stream_func = get_as_stream_func

    async def __aenter__(self) -> "AsyncStreamResponse":
        self._response = await self._get_as_stream_func()
        self._close = to_async(self._response.close)
        self._text = to_async(lambda: self._response.text)
        self._response_stream = ResponseStream(self._response)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._close()

    async def text(self) -> str:
        return await self._text()

    def iter_bytes(
        self, chunk_size: int = DEFAULT_CHUNK_SIZE, decode_unicode: bool = False
    ) -> AsyncIterator:
        response_iterator = self._response.iter_content(
            chunk_size=chunk_size, decode_unicode=decode_unicode
        )
        return AsyncIterator(response_iterator)

    @property
    def stream(self) -> io.BufferedIOBase:
        return self._response_stream

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def ok(self):
        return self._response.ok

    @property
    def is_redirect(self):
        return self._response.is_redirect


class AsyncHttpSession:
    _session: requests.Session

    _close: Callable[[], Awaitable[None]]
    _get: Callable[[str], Awaitable[requests.Response]]
    _post: Callable[[str], Awaitable[requests.Response]]
    _get_as_stream: Callable[[str], Awaitable[requests.Response]]

    _pop_header: Callable[[str], Awaitable[Optional[Union[str, bytes]]]]
    _update_header: Callable[[], Awaitable[None]]

    def __init__(
        self, retry_count: int, connect_timeout: int, read_timeout: int
    ) -> None:
        """
        Creates an asynchronous HTTP session with the given settings.

        :param retry_count: The number of retries in case of network failures.
        :param connect_timeout: The number of seconds the client will wait for establishing the connection to the server.
        :param read_timeout: The number of seconds the client will wait for the server to send a response. Specifically, it's the number of seconds that the client will wait between bytes sent from the server.
        """

        retries = requests.adapters.Retry(
            total=retry_count,
            backoff_factor=1,
            status_forcelist=[http.HTTPStatus.BAD_GATEWAY.value],
        )
        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": f"DataAccessPlatformClientLibrary/{__version__}"
        }
        self._session.mount(
            "https://", requests.adapters.HTTPAdapter(max_retries=retries)
        )

        self._close = to_async(self._session.close)

        timeout = (connect_timeout, read_timeout)
        self._get = to_async(partial(self._session.get, timeout=timeout))
        self._post = to_async(partial(self._session.post, timeout=timeout))
        self._get_as_stream = to_async(
            partial(self._session.get, stream=True, timeout=timeout)
        )

        self._pop_header = to_async(self._pop_header_sync)
        self._update_header = to_async(self._session.headers.update)

    async def close(self) -> None:
        await self._close()

    async def get(self, *args, **kwargs) -> requests.Response:
        """
        Performs a GET request to the given URL. Parameters are the same as for requests.get.
        """

        return await self._get(*args, **kwargs)

    async def post(self, *args, **kwargs) -> requests.Response:
        """
        Performs a POST request to the given URL. Parameters are the same as for requests.post.
        """

        return await self._post(*args, **kwargs)

    def get_as_stream(self, url: str) -> AsyncStreamResponse:
        """
        Performs a GET request to the given URL allowing the consumer to read the response as a stream.

        :param url: The given URL.
        :returns: An AsyncStreamResponse object that allows the consumer to be read as a stream.
        """
        return AsyncStreamResponse(partial(self._get_as_stream, url=url))

    async def pop_header(self, *args, **kwargs) -> Optional[Union[str, bytes]]:
        """
        Drops and returns the HTTP header with the given key.

        :param header_key: The name of the HTTP header to drop.
        :returns: The value of the dropped HTTP header.
        """
        return await self._pop_header(*args, **kwargs)

    async def update_headers(self, *args, **kwargs) -> None:
        """
        Sets the values of the given HTTP headers.

        :param headers: A dictionary containing the name and value of the HTTP headers to be set.
        """
        await self._update_header(*args, **kwargs)

    def _pop_header_sync(self, header_key: str) -> Optional[Union[str, bytes]]:
        if header_key in self._session.headers:
            return self._session.headers.pop(header_key)
        return None

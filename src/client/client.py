"""Client module."""

import pathlib
from collections.abc import AsyncIterator

import aiofiles
import grpc  # type: ignore[reportMissingTypeStubs]
from dependency_injector import containers, providers
from organizer.note.v1.note_service_pb2_grpc import NoteServiceStub

from src.client.config import NoteClientSettings


async def _aio_secure_channel(*args, **kwargs) -> AsyncIterator[grpc.aio.Channel]:
    """Creates a secure asynchronous Channel to a server.

    See `grpc.aio.secure_channel` for description of arguments.

    Yields:
        A secure asynchronous Channel to a server.
    """
    async with grpc.aio.secure_channel(*args, **kwargs) as channel:
        yield channel


async def _read_file_or_none(file: pathlib.Path | None) -> bytes | None:
    """Reads file as bytes or None for gRPC runtime compatibility.

    Args:
        file: Path to file.

    Returns:
        File content or None.
    """
    if not file:
        return None

    async with aiofiles.open(pathlib.Path(file), "rb") as read_file:
        return await read_file.read()


class GrpcNoteContainer(containers.DeclarativeContainer):
    """gRPC Note client dependency injection container."""

    config: NoteClientSettings = providers.Configuration(  # type: ignore[assignment]
        pydantic_settings=[NoteClientSettings()],  # type: ignore[call-arg]
        strict=True,
    )

    __root_certificates, __private_key, __certificate_chain = (
        providers.Resource(_read_file_or_none, file=config.grpc.root_certificates),
        providers.Resource(_read_file_or_none, file=config.grpc.private_key),
        providers.Resource(_read_file_or_none, file=config.grpc.certificate_chain),
    )

    __credentials: providers.Resource[grpc.ChannelCredentials] = providers.Resource(
        grpc.ssl_channel_credentials,
        root_certificates=__root_certificates,
        private_key=__private_key,
        certificate_chain=__certificate_chain,
    )

    __channel = providers.Resource(
        _aio_secure_channel,
        target=config.grpc.target,
        credentials=__credentials,
        options=config.grpc.options,
        compression=config.grpc.compression,
        interceptors=None,  # You can include interceptors here
    )

    client = providers.Singleton(NoteServiceStub, channel=__channel)

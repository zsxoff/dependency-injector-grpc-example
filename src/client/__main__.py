"""Main module."""

import asyncio

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from organizer.note.v1.note_service_pb2 import CreateNoteRequest, CreateNoteResponse, GetNoteRequest, GetNoteResponse
from organizer.note.v1.note_service_pb2_grpc import NoteServiceStub
from pydantic_settings import SettingsConfigDict

from src.base.channel import GrpcSingleSecureChannel
from src.base.config import GrpcClientSettings


class OrganizerClientSettings(GrpcClientSettings):
    """gRPC client settings."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="GRPC_ORGANIZER_CLIENT_", extra="ignore")


class OrganizerGrpcContainer(containers.DeclarativeContainer):
    """gRPC stubs dependency injection container."""

    # config
    config = providers.Configuration(pydantic_settings=[OrganizerClientSettings()], strict=True)  # type: ignore[call-arg]

    # gRPC channel
    channel_container = providers.Container(GrpcSingleSecureChannel, config=config)

    # stubs
    note_service_stub = providers.Singleton(NoteServiceStub, channel=channel_container.channel)


@inject
async def create_note(
    note_service_stub: NoteServiceStub = Provide[OrganizerGrpcContainer.note_service_stub],
) -> str:
    """Create note.

    Args:
        note_service_stub: Note gRPC service stub.

    Returns:
        str: Note ID.
    """
    create_note_response: CreateNoteResponse = await note_service_stub.CreateNote(CreateNoteRequest(content="Hi!"))

    return create_note_response.note_id


@inject
async def get_note(
    note_id: str,
    note_service_stub: NoteServiceStub = Provide[OrganizerGrpcContainer.note_service_stub],
) -> str:
    """Get note by ID.

    Args:
        note_id: Note ID.
        note_service_stub: Note gRPC service stub.

    Returns:
        str: Note content.
    """
    get_note_response: GetNoteResponse = await note_service_stub.GetNote(GetNoteRequest(note_id=note_id))

    return get_note_response.content


async def main() -> None:
    """Run gRPC client."""
    container = OrganizerGrpcContainer()
    container.check_dependencies()
    container.wire(modules=[__name__])

    await container.init_resources()  # type: ignore[misc] # Ignored because it's OK for Asynchronous initializers

    # Business logic here
    note_id = await create_note()
    content = await get_note(note_id)
    print(content)  # noqa: T201

    await container.shutdown_resources()  # type: ignore[misc] # Ignored because it's OK for Asynchronous initializers


if __name__ == "__main__":
    asyncio.run(main())

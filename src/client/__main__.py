"""gRPC client main."""

import asyncio

from dependency_injector.wiring import Provide, inject
from organizer.note.v1.note_service_pb2 import CreateNoteRequest, CreateNoteResponse
from organizer.note.v1.note_service_pb2_grpc import NoteServiceStub

from src.client.client import GrpcNoteContainer


@inject
async def run(
    note_client: NoteServiceStub = Provide[GrpcNoteContainer.client],
) -> None:
    """Runs gRPC note client.

    Args:
        note_client: Note gRPC client.
    """
    _: CreateNoteResponse = await note_client.CreateNote(CreateNoteRequest(content="Hello, World!"))


async def main() -> None:
    """Run gRPC client."""
    container = GrpcNoteContainer()
    container.check_dependencies()
    container.wire(modules=[__name__])

    await container.init_resources()  # type: ignore[misc] # Ignored because it's OK for Asynchronous initializers
    await run()
    await container.shutdown_resources()  # type: ignore[misc] # Ignored because it's OK for Asynchronous initializers
    await asyncio.sleep(1.0)


if __name__ == "__main__":
    asyncio.run(main())

"""Server config."""

import pathlib
from typing import Annotated

import grpc
from pydantic_settings import BaseSettings
from typing_extensions import Doc


class GrpcServerSettings(BaseSettings):
    """gRPC server settings."""

    address: Annotated[
        str,
        Doc(
            """
            The address for which to open a port. If the port is 0, or not specified in the address, then the gRPC
            runtime will choose a port.

            Required field.
            """
        ),
    ]

    secure: Annotated[
        bool,
        Doc(
            """
            Opens a secure port for accepting RPCs.

            Default: True.
            """
        ),
    ] = True

    private_key_certificate_chain_pairs: Annotated[
        list[tuple[pathlib.Path, pathlib.Path]] | None,
        Doc(
            """
            A list of pairs of the form [PEM-encoded private key, PEM-encoded certificate chain].

            Default: None.
            """
        ),
    ]

    root_certificates: Annotated[
        pathlib.Path | None,
        Doc(
            """
            An optional byte string of PEM-encoded client root certificates that the server will use to verify client
            authentication. If omitted, require_client_auth must also be False.

            Default: None.
            """
        ),
    ] = None

    require_client_auth: Annotated[
        bool,
        Doc(
            """
            A boolean indicating whether or not to require clients to be authenticated. May only be True if
            root_certificates is not None.

            Default: False,
            """
        ),
    ] = False

    maximum_concurrent_rpcs: Annotated[
        int | None,
        Doc(
            """
            The maximum number of concurrent RPCs this server will service before returning RESOURCE_EXHAUSTED status,
            or None to indicate no limit.

            Default: None.
            """
        ),
    ] = None

    options: Annotated[
        list[tuple[str, str]] | None,
        Doc(
            """
            An optional list of key-value pairs (:term:`channel_arguments` in gRPC runtime) to configure the channel.

            Default: None.
            """
        ),
    ] = None

    compression: Annotated[
        grpc.Compression,
        Doc(
            """
            Indicates the compression method to be used for an RPC.

            Values:
              - 0 - NoCompression
              - 1 - Deflate
              - 2 - Gzip

            Default: 0.
            """
        ),
    ] = grpc.Compression.NoCompression

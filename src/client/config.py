"""Config module."""

import pathlib
from typing import Annotated

import grpc
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Doc


class GrpcClientSettings(BaseSettings):
    """gRPC client settings."""

    target: Annotated[
        str,
        Doc(
            """
            gRPC server host.

            Required field.
            """
        ),
    ]

    root_certificates: Annotated[
        pathlib.Path | None,
        Doc(
            """
            The PEM-encoded root certificates as a byte string, or None to retrieve them from a default location chosen
            by gRPC runtime.

            Default: None.
            """
        ),
    ] = None

    private_key: Annotated[
        pathlib.Path | None,
        Doc(
            """
            The PEM-encoded private key as a byte string, or None if no private key should be used.

            Default: None.
            """
        ),
    ] = None

    certificate_chain: Annotated[
        pathlib.Path | None,
        Doc(
            """
            The PEM-encoded certificate chain as a byte string to use or None if no certificate chain should be used.

            Default: None.
            """
        ),
    ] = None

    options: Annotated[
        list[tuple[str, str]] | None,
        Doc(
            """
            An optional list of key-value pairs (channel_arguments in gRPC Core runtime) to configure the channel.

            Default: None.
            """
        ),
    ] = None

    compression: Annotated[
        grpc.Compression,
        Doc(
            """
            An optional value indicating the compression method to be used over the lifetime of the channel.

            Values:
              - 0 - NoCompression
              - 1 - Deflate
              - 2 - Gzip

            Default: 0.
            """
        ),
    ] = grpc.Compression.NoCompression


class NoteClientSettings(GrpcClientSettings):
    """gRPC client settings."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="GRPC_NOTE_CLIENT_", extra="ignore")

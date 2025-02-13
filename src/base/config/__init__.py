"""Config module."""

from src.base.config.client import GrpcClientSettings
from src.base.config.server import GrpcServerSettings


__all__ = [
    "GrpcClientSettings",
    "GrpcServerSettings",
]

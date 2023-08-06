from __future__ import annotations

from typing import TYPE_CHECKING

from .__routes__ import APIRoutes

if TYPE_CHECKING:
    from . import DiscordAPIClient

self: DiscordAPIClient = None
methods = (
    "b",
)

async def b(): pass
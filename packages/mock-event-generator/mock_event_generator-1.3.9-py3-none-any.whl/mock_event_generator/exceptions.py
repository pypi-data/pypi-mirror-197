"""Exceptions specific to the mock_event_generator package."""

__all__ = [
    'MEGIgnoreEventError',
    'MEGInvalidGraceDBAliasOrURLError',
]


class MEGIgnoreEventError(Exception):
    """When the G-event should be filtered out."""


class MEGInvalidGraceDBAliasOrURLError(ValueError):
    """When the GraceDB specifier is not a known alias nor a valid URL."""

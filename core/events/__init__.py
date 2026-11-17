"""Event envelope and upcasting, shared by all domain modules."""

from core.events.envelope import EventValidationError, validate_event
from core.events.upcast import upcast

__all__ = ["EventValidationError", "upcast", "validate_event"]

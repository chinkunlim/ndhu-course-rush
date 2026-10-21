"""Domain layer: pure data models with no I/O and no framework dependencies."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    """A course scheduled for selection.

    Attributes:
        index: Original row index on the web page.
        code: Course identifier code.
        name: Course title or name.
        limit: Maximum enrollment capacity.
        enrolled: Current number of enrolled students.
        remaining: Remaining seats available.
    """

    index: int
    code: str
    name: str
    limit: int
    enrolled: int
    remaining: int


@dataclass(frozen=True)
class CoursePriority:
    """User priority ranking for course selection.

    Attributes:
        priority: Priority ranking (lower numbers indicate higher priority).
        index: Original row index of the course.
    """

    priority: int
    index: int

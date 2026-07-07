"""
PawPal+ core logic layer.
Contains the data models and scheduling logic for the pet care app.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    frequency: str = "once"  # "once", "daily", "weekly"
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    """Represents a single pet and its list of care tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet's task list."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks belonging to this pet."""
        pass


@dataclass
class Owner:
    """Represents the pet owner, who manages one or more pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a new pet to this owner's list of pets."""
        pass

    def get_all_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        pass


class Scheduler:
    """
    The 'brain' of PawPal+. Reads tasks from an Owner's pets,
    sorts and organizes them, and generates a daily plan.
    """

    def __init__(self, owner: Owner, available_minutes: int = 480):
        self.owner = owner
        self.available_minutes = available_minutes

    def get_all_tasks(self) -> List[Task]:
        """Collect all tasks across every pet belonging to the owner."""
        pass

    def sort_by_priority(self) -> List[Task]:
        """Return all tasks sorted by priority (high to low)."""
        pass

    def generate_plan(self) -> List[Task]:
        """
        Build a daily plan that fits within available_minutes,
        prioritizing higher-priority tasks first.
        """
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why the plan looks the way it does."""
        pass

    def detect_conflicts(self) -> List[str]:
        """Detect and return warnings for any scheduling conflicts."""
        pass
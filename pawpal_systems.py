"""
PawPal+ core logic layer.
Contains the data models and scheduling logic for the pet care app.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    time: str  # scheduled time in "HH:MM" 24-hour format, e.g. "08:00"
    pet_name: str = ""  # which pet this task belongs to (set when added to a Pet)
    frequency: str = "once"  # "once", "daily", "weekly"
    is_complete: bool = False
    due_date: str = ""  # ISO date "YYYY-MM-DD", set for recurring tasks

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True


@dataclass
class Pet:
    """Represents a single pet and its list of care tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks


@dataclass
class Owner:
    """Represents the pet owner, who manages one or more pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a new pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets


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
        all_tasks = []
        for pet in self.owner.get_all_pets():
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def sort_by_priority(self) -> List[Task]:
        """Return all tasks sorted by priority (high to low)."""
        return sorted(
            self.get_all_tasks(),
            key=lambda t: PRIORITY_ORDER.get(t.priority, 99)
        )

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted chronologically by their time attribute."""
        return sorted(self.get_all_tasks(), key=lambda t: t.time)

    def filter_tasks(self, pet_name: Optional[str] = None,
                      completed: Optional[bool] = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = self.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.is_complete == completed]
        return tasks

    def generate_plan(self) -> List[Task]:
        """
        Build a daily plan that fits within available_minutes,
        prioritizing higher-priority tasks first (then earlier time as tiebreak).
        """
        candidates = sorted(
            self.get_all_tasks(),
            key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.time)
        )

        plan = []
        minutes_used = 0
        for task in candidates:
            if minutes_used + task.duration_minutes <= self.available_minutes:
                plan.append(task)
                minutes_used += task.duration_minutes

        return sorted(plan, key=lambda t: t.time)

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why the plan looks the way it does."""
        plan = self.generate_plan()
        all_tasks = self.get_all_tasks()
        skipped = [t for t in all_tasks if t not in plan]

        minutes_used = sum(t.duration_minutes for t in plan)
        lines = [
            f"Included {len(plan)} of {len(all_tasks)} tasks "
            f"({minutes_used}/{self.available_minutes} minutes used), "
            f"prioritizing high-priority tasks first."
        ]

        if skipped:
            lines.append("Skipped due to time budget or lower priority:")
            for task in skipped:
                lines.append(
                    f"  - {task.description} ({task.pet_name}, "
                    f"{task.priority} priority, {task.duration_minutes} min)"
                )
        else:
            lines.append("All tasks fit within the available time.")

        return "\n".join(lines)

    def detect_conflicts(self) -> List[str]:
        """Detect and return warnings for any scheduling conflicts (same time slot)."""
        warnings = []
        tasks = self.get_all_tasks()

        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time:
                    warnings.append(
                        f"Conflict at {tasks[i].time}: "
                        f"'{tasks[i].description}' ({tasks[i].pet_name}) "
                        f"overlaps with '{tasks[j].description}' ({tasks[j].pet_name})"
                    )

        return warnings

    def advance_recurring_task(self, task: Task) -> Optional[Task]:
        """
        If a completed task is daily or weekly, create and return
        a new Task instance for its next occurrence, with due_date
        calculated using timedelta. Returns None for one-time tasks.
        """
        if task.frequency not in ("daily", "weekly"):
            return None

        days_ahead = 1 if task.frequency == "daily" else 7
        next_due_date = date.today() + timedelta(days=days_ahead)

        next_task = Task(
            description=task.description,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            time=task.time,
            pet_name=task.pet_name,
            frequency=task.frequency,
            is_complete=False,
            due_date=next_due_date.isoformat(),
        )
        return next_task

    def complete_task(self, task: Task) -> Optional[Task]:
        """
        Mark a task complete and, if it's recurring, automatically
        create and attach its next occurrence to the correct pet.
        Returns the newly created task, or None for one-time tasks.
        """
        task.mark_complete()
        next_task = self.advance_recurring_task(task)

        if next_task:
            for pet in self.owner.get_all_pets():
                if pet.name == task.pet_name:
                    pet.add_task(next_task)
                    break

        return next_task
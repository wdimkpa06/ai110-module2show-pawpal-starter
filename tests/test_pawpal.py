"""
Automated tests for PawPal+ core logic.
"""

import pytest
from pawpal_systems import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    """Marking a task complete should update its is_complete flag."""
    task = Task(
        description="Feeding", duration_minutes=10,
        priority="high", time="08:00"
    )
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count."""
    pet = Pet(name="Biscuit", species="Dog")
    assert len(pet.get_tasks()) == 0

    task = Task(
        description="Morning walk", duration_minutes=30,
        priority="high", time="08:00"
    )
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    """Scheduler.sort_by_time() should return tasks earliest first."""
    owner = Owner(name="Alex")
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Evening walk", duration_minutes=30,
                       priority="medium", time="18:00"))
    pet.add_task(Task(description="Morning walk", duration_minutes=30,
                       priority="high", time="08:00"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert [t.time for t in sorted_tasks] == ["08:00", "18:00"]


def test_detect_conflicts_flags_same_time_tasks():
    """Scheduler.detect_conflicts() should flag two tasks at the same time."""
    owner = Owner(name="Alex")
    biscuit = Pet(name="Biscuit", species="Dog")
    whiskers = Pet(name="Whiskers", species="Cat")
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    biscuit.add_task(Task(description="Morning walk", duration_minutes=30,
                           priority="high", time="08:00"))
    whiskers.add_task(Task(description="Feeding", duration_minutes=10,
                            priority="high", time="08:00"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1


def test_pet_with_no_tasks_has_empty_list():
    """A pet with no tasks should return an empty list, not an error."""
    pet = Pet(name="Whiskers", species="Cat")
    assert pet.get_tasks() == []
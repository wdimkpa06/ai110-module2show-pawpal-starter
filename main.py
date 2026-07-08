"""
Demo script for PawPal+.
Creates an owner, pets, and tasks, then prints a daily schedule,
plan explanation, and any conflicts found.
"""

from pawpal_systems import Owner, Pet, Task, Scheduler


def print_task_list(title, tasks):
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("  (none)")
        return
    for task in tasks:
        status = "done" if task.is_complete else "pending"
        print(
            f"  {task.time} | {task.pet_name:<10} | {task.description:<20} "
            f"| {task.duration_minutes:>3} min | {task.priority:<6} | {status}"
        )


def main():
    # Set up an owner with two pets
    owner = Owner(name="Alex")

    biscuit = Pet(name="Biscuit", species="Dog")
    whiskers = Pet(name="Whiskers", species="Cat")

    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    # Add tasks out of order, with a mix of priorities and one deliberate conflict
    biscuit.add_task(Task(
        description="Morning walk", duration_minutes=30,
        priority="high", time="08:00", frequency="daily"
    ))
    biscuit.add_task(Task(
        description="Evening walk", duration_minutes=30,
        priority="medium", time="18:00", frequency="daily"
    ))
    whiskers.add_task(Task(
        description="Feeding", duration_minutes=10,
        priority="high", time="08:00", frequency="daily"
    ))
    whiskers.add_task(Task(
        description="Litter box cleaning", duration_minutes=10,
        priority="low", time="12:00", frequency="daily"
    ))
    biscuit.add_task(Task(
        description="Vet checkup", duration_minutes=45,
        priority="high", time="10:00", frequency="once"
    ))

    scheduler = Scheduler(owner, available_minutes=90)

    print_task_list("All tasks (sorted by time)", scheduler.sort_by_time())
    print_task_list("All tasks (sorted by priority)", scheduler.sort_by_priority())

    print("\nToday's Plan")
    print("-" * 12)
    plan = scheduler.generate_plan()
    print_task_list("Selected for today's plan", plan)

    print("\nPlan Explanation")
    print("-" * 16)
    print(scheduler.explain_plan())

    print("\nConflict Check")
    print("-" * 14)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  WARNING: {warning}")
    else:
        print("  No conflicts found.")

    print("\nRecurrence Check")
    print("-" * 16)
    daily_task = biscuit.get_tasks()[0]  # "Morning walk", a daily task
    print(f"Marking '{daily_task.description}' complete...")
    next_occurrence = scheduler.complete_task(daily_task)
    if next_occurrence:
        print(
            f"  Created next occurrence: '{next_occurrence.description}' "
            f"due {next_occurrence.due_date} at {next_occurrence.time}"
        )
    print_task_list("Biscuit's tasks after completion", biscuit.get_tasks())

if __name__ == "__main__":
    main()
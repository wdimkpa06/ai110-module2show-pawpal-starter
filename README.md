# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

All tasks (sorted by time)
--------------------------
  08:00 | Biscuit    | Morning walk         |  30 min | high   | pending
  08:00 | Whiskers   | Feeding              |  10 min | high   | pending
  10:00 | Biscuit    | Vet checkup          |  45 min | high   | pending
  12:00 | Whiskers   | Litter box cleaning  |  10 min | low    | pending
  18:00 | Biscuit    | Evening walk         |  30 min | medium | pending

All tasks (sorted by priority)
------------------------------
  08:00 | Biscuit    | Morning walk         |  30 min | high   | pending
  10:00 | Biscuit    | Vet checkup          |  45 min | high   | pending
  08:00 | Whiskers   | Feeding              |  10 min | high   | pending
  18:00 | Biscuit    | Evening walk         |  30 min | medium | pending
  12:00 | Whiskers   | Litter box cleaning  |  10 min | low    | pending

Today's Plan
------------

Selected for today's plan
-------------------------
  08:00 | Biscuit    | Morning walk         |  30 min | high   | pending
  08:00 | Whiskers   | Feeding              |  10 min | high   | pending
  10:00 | Biscuit    | Vet checkup          |  45 min | high   | pending

Plan Explanation
----------------
Included 3 of 5 tasks (85/90 minutes used), prioritizing high-priority tasks first.
Skipped due to time budget or lower priority:
  - Evening walk (Biscuit, medium priority, 30 min)
  - Litter box cleaning (Whiskers, low priority, 10 min)

Conflict Check
--------------
  WARNING: Conflict at 08:00: 'Morning walk' (Biscuit) overlaps with 'Feeding' (Whiskers)

Recurrence Check
----------------
Marking 'Morning walk' complete...
  Created next occurrence: 'Morning walk' due 2026-07-08 at 08:00

Biscuit's tasks after completion
--------------------------------
  08:00 | Biscuit    | Morning walk         |  30 min | high   | done
  18:00 | Biscuit    | Evening walk         |  30 min | medium | pending
  10:00 | Biscuit    | Vet checkup          |  45 min | high   | pending
  08:00 | Biscuit    | Morning walk         |  30 min | high   | pending


## 🧪 Testing PawPal+

```bash
python -m pytest
```

This suite covers task completion, task addition, sorting by time, conflict detection,
recurring task creation, one-time tasks not recurring, time-budget enforcement in plan
generation, filtering by completion status, and a pet with no tasks (edge case).

**Confidence Level:** (4/5 stars) — core behaviors are well covered, but I haven't
tested overlapping-duration conflicts (only exact time matches) or weekly recurrence
specifically, since my tests focus on daily recurrence.

Sample test output:

```
# Paste your pytest output here
```
============================================================================== test session starts ==============================================================================
platform win32 -- Python 3.13.14, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\omadi\Documents\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0, dash-4.1.0, timeout-2.4.0
collected 9 items                                                                                                                                                                

tests\test_pawpal.py .........                                                                                                                                             [100%]

=============================================================================== 9 passed in 0.13s ===============================================================================

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | Sorts all tasks chronologically or by priority (high → medium → low) |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Filters tasks by pet name and/or completion status, combinable |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks scheduled at the exact same time, even across different pets |
| Recurring tasks | `Scheduler.complete_task()`, `Scheduler.advance_recurring_task()` | Marking a daily/weekly task complete auto-creates its next occurrence using `timedelta` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter an owner name, pet name, and species, then click "Set up owner and pet." This creates the Owner and Pet objects and stores them in Streamlit's session state so they persist across interactions.
2. Add care tasks using the form: a title, duration, priority, time (HH:MM), and frequency (once/daily/weekly). Each task is added directly to the Pet object via `Pet.add_task()`.
3. Added tasks appear immediately in a table below the form, showing time, duration, priority, frequency, and completion status.
4. Adjust the "Available time today" slider to set how many minutes the Scheduler has to work with.
5. Click "Generate schedule." This calls `Scheduler.generate_plan()`, which greedily selects tasks by priority until the time budget is used up, `Scheduler.explain_plan()`, which describes why each task was included or skipped, and `Scheduler.detect_conflicts()`, which flags any tasks scheduled at the same time.
6. Results are displayed as: a table of the day's plan, a plain-language explanation, and either a success message (no conflicts) or warning messages (one per conflict found).

Key Scheduler behaviors demonstrated: priority-based plan generation within a time budget, human-readable plan explanations, and same-time conflict detection across pets.

All tasks (sorted by time)
--------------------------
  08:00 | Biscuit    | Morning walk         |  30 min | high   | pending
  08:00 | Whiskers   | Feeding              |  10 min | high   | pending
  10:00 | Biscuit    | Vet checkup          |  45 min | high   | pending
  12:00 | Whiskers   | Litter box cleaning  |  10 min | low    | pending
  18:00 | Biscuit    | Evening walk         |  30 min | medium | pending

All tasks (sorted by priority)
------------------------------
  08:00 | Biscuit    | Morning walk         |  30 min | high   | pending
  10:00 | Biscuit    | Vet checkup          |  45 min | high   | pending
  08:00 | Whiskers   | Feeding              |  10 min | high   | pending
  18:00 | Biscuit    | Evening walk         |  30 min | medium | pending
  12:00 | Whiskers   | Litter box cleaning  |  10 min | low    | pending

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

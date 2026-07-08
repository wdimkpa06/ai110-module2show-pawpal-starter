# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design uses four classes: Owner (holds the pet owner's name and their list of pets), Pet (holds the pet's name, species, and list of tasks), Task (holds a description, duration, priority, frequency, and completion status), and Scheduler (reads tasks from the Owner's pets, sorts them by priority, and generates a daily plan that fits within the available time, explaining its choices along the way).

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After an AI review of my initial skeleton, I added a time field and a pet_name field to the Task class. Originally, Task only tracked duration, which made it impossible to detect scheduling conflicts (two tasks at the same time) or calculate the next occurrence of a recurring task. Adding pet_name also lets a flattened list of tasks (returned by Scheduler.get_all_tasks()) still identify which pet each task belongs to, which matters for readable output.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers task duration, priority level, and available time budget when building a plan. It also considers scheduled time when detecting conflicts. Priority mattered most to me because a pet owner with limited time should never miss a high-priority task (like medication) in favor of a low-priority one (like grooming), even if the low-priority task fits more neatly into the schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler uses a greedy algorithm: it sorts tasks by priority, then adds them to the plan in that order until the time budget runs out. This means a lower-priority task could be skipped even if it would technically fit alongside a slightly different combination of higher-priority tasks (a true optimal-fit solution would require something closer to a knapsack algorithm). I chose the greedy approach because it's simpler to implement, easier to explain to a user via explain_plan(), and prioritizing strictly by importance matches how a real pet owner would think about their day, rather than optimizing purely for "most tasks completed."
My conflict detection also only checks for exact time matches rather than overlapping duration ranges — two tasks at 08:00 and 08:15 with 30-minute durations would actually overlap in real life but wouldn't be flagged. I accepted this simplification for now since it covers the most obvious case (double-booking the same time slot) without the added complexity of interval overlap logic.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

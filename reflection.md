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

I used my AI assistant throughout the project: drafting the initial Mermaid UML diagram from a description of my classes, fleshing out the core implementation of my four classes in pawpal_system.py, and writing the main.py demo script. The most effective use was asking it to review my class skeleton after Phase 1 and point out missing relationships before I wrote the real logic, that caught a real gap early instead of after the fact.

The most helpful prompts were the ones that gave it full context and asked for a specific judgment call, not just "write code for X." For example, asking it to review my finished skeleton and point out gaps was more valuable than asking it to write the skeleton in the first place, because that's the step where a second perspective actually catches design flaws instead of just producing text. Similarly, asking "why is this test failing, and is the bug in my test or my logic" was more useful than just asking it to fix a failing test, because it forced a diagnosis rather than a patch.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When the AI implemented generate_plan(), it used a greedy algorithm: sort all tasks by priority, then add them to the plan in that order until the time budget runs out. I didn't just accept this as the final word — I thought through whether it actually produces the best possible plan, and realized it doesn't. A true optimal-fit solution (closer to a knapsack algorithm) could sometimes pack more total value into the same time budget by skipping one large high-priority task in favor of several smaller medium-priority ones. The AI's implementation doesn't do that; it strictly respects priority order over maximizing how much fits.

I decided to keep the greedy version anyway, but only after evaluating the tradeoff myself rather than accepting the code because it worked. I verified my understanding by testing it directly: in my main.py demo, a 90-minute budget with three high-priority tasks correctly filled 85 of 90 minutes and skipped a medium and a low priority task, even though the medium-priority task alone might have fit into leftover time under a different strategy. I concluded the greedy approach was actually the right choice for this use case, not just the easiest one, a pet owner would want their most important tasks guaranteed a spot, not a plan that's been shuffled around purely to maximize the count of completed tasks. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested: marking a task complete, adding a task to a pet, sorting tasks chronologically, detecting conflicts between tasks at the same time (even across different pets), recurring task creation (a completed daily task spawns its next occurrence with the correct due date), one-time tasks correctly not recurring, the scheduler never exceeding its time budget, filtering tasks by completion status, and a pet with zero tasks not causing errors. These matter because they cover both the "happy path" (normal usage) and edge cases (empty data, boundary conditions on the time budget) that a real pet owner's usage patterns would likely hit.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident (4/5) the core scheduling logic works correctly, since all 9 tests pass and I manually verified the same behaviors in both the CLI and the Streamlit UI. If I had more time, I'd test: conflict detection for overlapping (not just identical) time ranges, weekly recurrence specifically (I only tested daily), and what happens when two tasks have the exact same priority and time (a tiebreak edge case).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the conflict detection and plan explanation features, since they make the app feel useful rather than just being a data tracker, a real pet owner would actually want to know why a task got skipped, not just that it did.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

With another iteration, I'd improve the conflict detection to check for overlapping time ranges instead of exact time matches, and I'd move away from string-based times ("08:00") toward proper datetime objects, which would make duration-aware overlap checking and more robust date math much easier.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that being the "lead architect" means catching structural gaps before they become bugs, like realizing Task needed a time field before conflict detection was even attempted, rather than just accepting whatever the AI generates first. AI is fast at producing working code, but deciding what the code actually needs to do, and verifying that it does it correctly, is still on me.
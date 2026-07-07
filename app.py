import streamlit as st
from pawpal_systems import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, a pet care planning assistant. Add your pet's care tasks below
and generate a daily plan based on priority and available time.
"""
)

# --- Session state setup ---
# Streamlit reruns the whole script on every interaction, so we store the
# Owner object in session_state to make sure it persists across reruns
# instead of being recreated (and emptied) every time.
if "owner" not in st.session_state:
    st.session_state.owner = None

st.divider()

# --- Owner and Pet setup ---
st.subheader("Owner and Pet")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Set up owner and pet"):
    owner = Owner(name=owner_name)
    pet = Pet(name=pet_name, species=species)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Created owner '{owner_name}' with pet '{pet_name}'.")

st.divider()

# --- Task entry ---
st.subheader("Tasks")

if st.session_state.owner is None:
    st.info("Set up an owner and pet above before adding tasks.")
else:
    st.caption("Add care tasks for your pet. These feed directly into the scheduler.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        task_time = st.text_input("Time (HH:MM)", value="08:00")

    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        pet = st.session_state.owner.get_all_pets()[0]
        new_task = Task(
            description=task_title,
            duration_minutes=int(duration),
            priority=priority,
            time=task_time,
            frequency=frequency,
        )
        pet.add_task(new_task)
        st.success(f"Added '{task_title}' at {task_time}.")

    pet = st.session_state.owner.get_all_pets()[0]
    if pet.get_tasks():
        st.write("Current tasks:")
        task_rows = [
            {
                "Time": t.time,
                "Task": t.description,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Complete": t.is_complete,
            }
            for t in pet.get_tasks()
        ]
        st.table(task_rows)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule generation ---
st.subheader("Build Schedule")

available_minutes = st.slider("Available time today (minutes)", min_value=30, max_value=600, value=120, step=15)

if st.session_state.owner is None:
    st.info("Set up an owner and pet, then add tasks, before generating a schedule.")
else:
    if st.button("Generate schedule"):
        scheduler = Scheduler(st.session_state.owner, available_minutes=available_minutes)

        plan = scheduler.generate_plan()
        conflicts = scheduler.detect_conflicts()

        if plan:
            st.markdown("### Today's Plan")
            plan_rows = [
                {
                    "Time": t.time,
                    "Task": t.description,
                    "Pet": t.pet_name,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                }
                for t in plan
            ]
            st.table(plan_rows)
        else:
            st.info("No tasks fit in the available time. Try adding tasks or increasing available time.")

        st.markdown("### Why this plan?")
        st.write(scheduler.explain_plan())

        if conflicts:
            st.markdown("### Conflicts")
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts found.")
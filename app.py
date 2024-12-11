import streamlit as st
import sqlite3
import pandas as pd


# Database functions
def create_table():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            start_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            persons_responsible TEXT NOT NULL,
            status TEXT DEFAULT 'Not Started'
        )
    ''')
    conn.commit()
    conn.close()


def add_task(task, start_date, due_date, persons_responsible, status):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task, start_date, due_date, persons_responsible, status) VALUES (?, ?, ?, ?, ?)',
              (task, start_date, due_date, persons_responsible, status))
    conn.commit()
    conn.close()


def view_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    data = c.fetchall()
    conn.close()
    return data


def update_task(task_id, task, start_date, due_date, persons_responsible, status):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''
        UPDATE tasks 
        SET task = ?, start_date = ?, due_date = ?, persons_responsible = ?, status = ?
        WHERE id = ?
    ''', (task, start_date, due_date, persons_responsible, status, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()


create_table()
st.set_page_config(page_title="🎯 Task Manager", layout="wide")

st.markdown(
    """
    <style>
    .main-header {
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #F8F9FA;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="main-header">🎯 Task Management App</div>', unsafe_allow_html=True)

tabs = st.tabs(["➕ Add Task", "📋 View Tasks", "✏️ Update Task", "🗑️ Delete Task", "📊 Reports"])

with tabs[0]:
    st.header("Add New Task")
    with st.form(key="add_task_form"):
        task = st.text_input("Task Details 📝")
        start_date = st.date_input("Start Date 📅")
        due_date = st.date_input("Due Date 📅")
        persons_responsible = st.text_input("Persons Responsible 👤 (comma-separated)")
        status = st.selectbox("Status 🏷️", ["Not Started", "In-Progress", "Completed"], index=0)
        submitted = st.form_submit_button("Add Task ✅")

        if submitted:
            if task and start_date and due_date and persons_responsible:
                if due_date >= start_date:
                    add_task(task, str(start_date), str(due_date), persons_responsible, status)
                    st.success("Task added successfully! 🎉")
                else:
                    st.error("Due Date must be greater than or equal to Start Date.")
            else:
                st.error("All fields are required!")

with tabs[1]:
    st.header("View Tasks")
    tasks = view_tasks()
    if tasks:
        df = pd.DataFrame(tasks, columns=["ID", "Task", "Start Date", "Due Date", "Persons Responsible", "Status"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No tasks available. Add some to get started! 💡")

with tabs[2]:
    st.header("Update Existing Task")
    task_id = st.number_input("Enter Task ID to Update 🔢", min_value=1, step=1)
    update_task_name = st.text_input("New Task Name 📝")
    update_start_date = st.date_input("New Start Date 📅")
    update_due_date = st.date_input("New Due Date 📅")
    update_persons = st.text_input("New Responsible Persons 👤")
    update_status = st.selectbox("New Status 🏷️", ["Not Started", "In-Progress", "Completed"])
    if st.button("Update Task ✏️"):
        if update_task_name and update_start_date and update_due_date and update_persons:
            if update_due_date >= update_start_date:
                update_task(task_id, update_task_name, str(update_start_date), str(update_due_date), update_persons,
                            update_status)
                st.success("Task updated successfully! 🎉")
            else:
                st.error("Due Date must be greater than or equal to Start Date.")
        else:
            st.error("All fields are required!")

with tabs[3]:
    st.header("Delete a Task")
    delete_task_id = st.number_input("Enter Task ID to Delete 🔢", min_value=1, step=1)
    if st.button("Delete Task 🗑️"):
        delete_task(delete_task_id)
        st.success("Task deleted successfully! ✅")

with tabs[4]:
    st.header("Reports 📊")
    st.subheader("Tasks by Status")
    tasks = view_tasks()
    if tasks:
        df = pd.DataFrame(tasks, columns=["ID", "Task", "Start Date", "Due Date", "Persons Responsible", "Status"])
        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)
    else:
        st.info("No data available for reports! 📈")

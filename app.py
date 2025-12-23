import streamlit as st
import pandas as pd
from main import StudentManagementSystem

# Page Config
st.set_page_config(page_title="Student Management System", layout="wide")

# Initialize Backend
if 'sms' not in st.session_state:
    st.session_state.sms = StudentManagementSystem()

sms = st.session_state.sms

# Title
st.title("🎓 Student Management System")

# Sidebar - Add Student
st.sidebar.header("Add New Student")
with st.sidebar.form("add_student_form"):
    sid = st.text_input("ID")
    name = st.text_input("Name")
    age = st.text_input("Age")
    course = st.text_input("Course")
    marks = st.text_input("Marks")
    
    submitted = st.form_submit_button("Add Student")
    if submitted:
        if sid and name and age and course and marks:
            success, msg = sms.add_student(sid, name, age, course, marks)
            if success:
                st.success(msg)
                sms.save_data() # Auto-save
            else:
                st.error(msg)
        else:
            st.warning("All fields are required.")

# Sidebar - Actions
st.sidebar.markdown("---")
if st.sidebar.button("Save Data Manually"):
    success, msg = sms.save_data()
    st.toast(msg)

# Main Area - Search & View
col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input("🔍 Search by Name", "")

# Logic to get data
all_students = sms.get_all_students()

# Search Logic
if search_query:
    display_data = sms.search_student(search_query)
else:
    display_data = all_students

# Display Data
if display_data:
    df = pd.DataFrame(display_data, columns=["ID", "Name", "Age", "Course", "Marks"])
    
    # Use Data Editor for simple updates/deletes in future, but for now just display
    # Making ID the index
    df.set_index("ID", inplace=True)
    
    st.subheader("Student Records")
    st.dataframe(df, use_container_width=True)

    # Delete Section
    st.markdown("---")
    st.subheader("❌ Delete Student")
    del_col1, del_col2 = st.columns([3, 1])
    with del_col1:
        del_id = st.selectbox("Select ID to Delete", options=df.index.tolist(), key="del_select")
    with del_col2:
        if st.button("Delete"):
            success, msg = sms.delete_student(del_id)
            if success:
                st.success(msg)
                sms.save_data()
                st.rerun()
            else:
                st.error(msg)
                
    # Update Section (Simple version)
    st.markdown("---")
    st.subheader("✏️ Update details")
    up_col1, up_col2, up_col3 = st.columns(3)
    
    with up_col1:
        up_id = st.selectbox("Select ID to Update", options=df.index.tolist(), key="up_select")
    with up_col2:
        field = st.selectbox("Field", ["Name", "Age", "Course", "Marks"])
    with up_col3:
        new_val = st.text_input("New Value")
        
    if st.button("Update"):
        if new_val:
            success, msg = sms.update_student(up_id, field, new_val)
            if success:
                st.success(msg)
                sms.save_data()
                st.rerun()
            else:
                st.error(msg)
        else:
            st.warning("Please enter a new value.")

else:
    st.info("No students found.")

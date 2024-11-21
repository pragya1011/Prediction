# -*- coding: utf-8 -*-
"""Students_Performance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17RpWu_7weSpWF34owjnHYdXN7_qLvg99
"""

# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset from a Google Drive link
@st.cache
def load_data():
    # Replace with your public Google Drive link
    gdrive_link = "https://drive.google.com/uc?id=1HnLCBBbmV3MRrSPARsFOx6kZCqpUCPEo"  # Replace FILE_ID with the actual ID
    data = pd.read_csv(gdrive_link)
    # Replace binary values and map grades
    data['Gender'] = data['Gender'].replace({0: "Male", 1: "Female"})
    data['Tutoring'] = data['Tutoring'].replace({0: "No", 1: "Yes"})
    data['Extracurricular'] = data['Extracurricular'].replace({0: "No", 1: "Yes"})
    grade_mapping = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
    data['GradeClass'] = data['GradeClass'].map(grade_mapping)
    return data

student_data = load_data()

# Administrator View
def administrator_view(data):
    st.subheader("Administrator Dashboard")
    total_students = len(data['StudentID'].unique())
    avg_gpa = data['GPA'].mean()
    grade_counts = data['GradeClass'].value_counts()

    st.write(f"**Total Students:** {total_students}")
    st.write(f"**Average GPA:** {avg_gpa:.2f}")
    st.write("**Students by Grade:**")
    st.bar_chart(grade_counts)

# Teacher View
def teacher_view(data):
    st.subheader("Teacher Dashboard")
    student_id = st.selectbox("Select Student ID", data['StudentID'])
    student_details = data[data['StudentID'] == student_id]
    st.write("### Student Details")
    st.dataframe(student_details)

    if st.button("View Graphical Representation"):
        st.write("Graphical Representation of Student Details")
        student_details = student_details.drop(columns=['StudentID']).T
        student_details.columns = ['Value']
        fig, ax = plt.subplots()
        student_details.plot(kind='bar', legend=False, ax=ax, color='skyblue')
        plt.title("Student Details")
        st.pyplot(fig)

# Student View
def student_view(data):
    st.subheader("Student Dashboard")
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    age = st.selectbox("Select Age", list(range(10, 21)))
    if age < 15 or age > 18:
        st.error("Chosen wrong value, kindly choose between 15 and 18.")
        return
    study_time = st.selectbox("Study Time Weekly", ["0-5", "5-10", "10-15", "15-20"])
    absences = st.selectbox("Absences", ["0-5", "5-10", "10-15", "15-20", "25-30"])
    tutoring = st.selectbox("Tutoring", ["No", "Yes"])
    extracurricular = st.selectbox("Extracurricular", ["No", "Yes"])

    # Filter data based on input
    filtered_data = data[
        (data['Gender'] == gender) &
        (data['Age'] == age)
    ]

    if len(filtered_data) == 0:
        st.warning("No data found for the selected inputs.")
        return

    # Predict GPA and Grade (Approximation using mean values)
    predicted_gpa = filtered_data['GPA'].mean()
    predicted_grade = filtered_data['GradeClass'].mode()[0]

    st.write(f"**Predicted GPA:** {predicted_gpa:.2f}")
    st.write(f"**Predicted Grade:** {predicted_grade}")

    # Recommendation based on Grade
    grade_message = {
        "A": "Performed well, keep it up!",
        "B": "Working hard, do not stop now.",
        "C": "Chances of going higher, stay motivated.",
        "D": "Can do better, work harder and put more effort.",
        "E": "Needs improvement, focus on priorities."
    }
    st.write(f"**Recommendation:** {grade_message[predicted_grade]}")

# Main App
st.title("Student Performance Prediction Model")
st.sidebar.title("Options")
option = st.sidebar.selectbox("Choose", ["Administrator", "Teacher", "Student"])

if option == "Administrator":
    administrator_view(student_data)
elif option == "Teacher":
    teacher_view(student_data)
elif option == "Student":
    student_view(student_data)
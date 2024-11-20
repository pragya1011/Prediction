# -*- coding: utf-8 -*-
"""Students_Performance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17RpWu_7weSpWF34owjnHYdXN7_qLvg99
"""

import pandas as pd
import streamlit as st
import gdown  # To download the dataset from Google Drive
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Step 1: Load dataset from Google Drive
url = "https://drive.google.com/uc?id=1HnLCBBbmV3MRrSPARsFOx6kZCqpUCPEo"
output = "student_data.csv"
gdown.download(url, output, quiet=False)

# Load the dataset
student_data = pd.read_csv(output)

# Step 2: Streamlit Interface
st.title("Student Performance Prediction Model")

# Dropdown for User Role
role = st.selectbox("Choose", ["Student", "Teacher"])

if role == "Teacher":
    student_ids = student_data["StudentID"].tolist()
    selected_id = st.selectbox("Select Student ID", student_ids)
    if selected_id:
        details = student_data[student_data["StudentID"] == selected_id]
        st.write("Student Details:")
        st.write(details)

elif role == "Student":
    # User input for each feature
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    gender_binary = 0 if gender == "Male" else 1

    study_time = st.selectbox("Study Time Weekly (hours)", ["0-5", "5-10", "10-15", "15-20"])
    study_time_range = [int(x) for x in study_time.split("-")]

    absences = st.selectbox("Absences", ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30"])
    absences_range = [int(x) for x in absences.split("-")]

    tutoring = st.selectbox("Tutoring", ["No", "Yes"])
    tutoring_binary = 0 if tutoring == "No" else 1

    extracurricular = st.selectbox("Extracurricular", ["No", "Yes"])
    extracurricular_binary = 0 if extracurricular == "No" else 1

    # Step 3: Predict GPA and GradeClass
    if st.button("Predict Performance"):
        # Prepare data for prediction using only the selected features
        # Only use the features that were specified earlier (Gender, StudyTime, Absences, Tutoring, Extracurricular)
        X = student_data[["Gender", "StudyTimeWeekly", "Absences", "Tutoring", "Extracurricular"]]
        y_gpa = student_data["GPA"]
        y_grade = student_data["GradeClass"]

        # Train-Test Split
        X_train, X_test, y_gpa_train, y_gpa_test, y_grade_train, y_grade_test = train_test_split(
            X, y_gpa, y_grade, test_size=0.2, random_state=42
        )

        # Train Models
        gpa_model = RandomForestRegressor(random_state=42)
        gpa_model.fit(X_train, y_gpa_train)

        grade_model = RandomForestRegressor(random_state=42)
        grade_model.fit(X_train, y_grade_train)

        # Ensure the prediction input matches the columns in X_train
        input_data = pd.DataFrame([{
            "Gender": gender_binary,
            "StudyTimeWeekly": study_time_range[0],  # Approximation using range start
            "Absences": absences_range[0],    # Approximation using range start
            "Tutoring": tutoring_binary,
            "Extracurricular": extracurricular_binary
        }])

        # Make Predictions
        predicted_gpa = gpa_model.predict(input_data)[0]
        predicted_grade = grade_model.predict(input_data)[0]

        # Display Results
        st.write(f"Predicted GPA: {predicted_gpa:.2f}")
        st.write(f"Predicted Grade Class: {int(predicted_grade)}")